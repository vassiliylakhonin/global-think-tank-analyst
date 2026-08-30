import pytest
from gtta.resources import get_mode_template, get_skill_prompt


def test_packaged_skill_resources_are_complete():
    assert len(get_skill_prompt("en")) > 20_000
    assert len(get_skill_prompt("ru")) > 5_000
    mode_g = get_mode_template("G")
    assert "### Mode G" in mode_g
    assert "## Default memo output" not in mode_g


def test_skill_resource_language_is_explicit():
    with pytest.raises(ValueError, match="Unsupported language"):
        get_skill_prompt("de")


def test_langchain_prompt():
    pytest.importorskip("langchain_core")
    from gtta.langchain import get_system_prompt

    prompt = get_system_prompt(language="en")
    assert prompt is not None
    assert "Evidence mode" in prompt.content


def test_langchain_ru_prompt():
    pytest.importorskip("langchain_core")
    from gtta.langchain import get_system_prompt

    prompt = get_system_prompt(language="ru")
    assert prompt is not None
    assert len(prompt.content) > 1000


def test_llamaindex_prompt():
    pytest.importorskip("llama_index")
    from gtta.llamaindex import get_system_message

    msg = get_system_message(language="en")
    assert msg.role.value == "system"
    assert "Evidence mode" in msg.content


def test_extra_instructions():
    pytest.importorskip("langchain_core")
    from gtta.langchain import get_system_prompt

    prompt = get_system_prompt(extra_instructions="Focus on logistics.")
    assert "Focus on logistics." in prompt.content


def test_mcp_contract_preflight_tool():
    import asyncio
    pytest.importorskip("mcp")
    from gtta.mcp_server import app, check_memo_contract

    # Missing tags
    result_fail = asyncio.run(check_memo_contract("Just some text."))
    assert result_fail["passed"] is False
    assert "GTTA002" in {item["rule_id"] for item in result_fail["findings"]}

    # Valid text
    valid_text = "Evidence mode: reasoning-only\n[analyst-judgment] Some thought.\nModerate confidence."
    result_pass = asyncio.run(check_memo_contract(valid_text))
    assert result_pass["passed"] is True
    assert "No factuality" in result_pass["limitations"]

    tools = asyncio.run(app.list_tools())
    assert {tool.name for tool in tools} == {
        "check_memo_contract",
        "get_mode_template",
        "get_skill_prompt",
    }


def test_unit_economics_calculation():
    from gtta.economics import calculate_unit_economics, calculate_cost

    cost = calculate_cost(1000, 500, model_name="deepseek-chat")
    assert cost > 0
    assert cost < 0.01

    econ = calculate_unit_economics(
        input_text="Sample input about sanctions on Middle Corridor." * 50,
        output_text="Sample output memo with executive summary and scenarios." * 100,
    )
    assert econ["total_tokens"] > 0
    assert econ["estimated_query_cost_usd"] > 0
    assert econ["estimated_cascading_savings_pct"] >= 0.0
    assert econ["estimation_method"] == "character_count_divided_by_four"
    assert "gross_margin_pct" not in econ


def test_illustrative_knowledge_lookup_has_sources_and_freshness_warning():
    from gtta.knowledge import lookup_regional_knowledge

    res = lookup_regional_knowledge(
        "What is the impact of Middle Corridor transport bottleneck in Aktau?"
    )
    assert "ILLUSTRATIVE CONTEXT: MIDDLE_CORRIDOR" in res
    assert "Kazakhstan Temir Zholy" in res
    assert "Freshness: verify current primary sources" in res

    res_cbam = lookup_regional_knowledge("EU CBAM impact on Kazakh metals")
    assert "ILLUSTRATIVE CONTEXT: CBAM_KAZAKHSTAN" in res_cbam
    assert "taxation-customs.ec.europa.eu" in res_cbam


def test_agent_module_has_no_code_execution_tool():
    """The researcher node once built Python source from the user-supplied topic
    and handed it to PythonREPLTool, which made `topic` a remote code-execution
    vector through the FastAPI memo route. Keep the interpreter out of the graph.
    """
    from pathlib import Path

    import gtta.agent as agent_module

    source = Path(agent_module.__file__).read_text(encoding="utf-8")
    assert "PythonREPLTool" not in source
    assert "langchain_experimental" not in source


def test_memo_route_is_gated_when_an_api_key_is_set(monkeypatch):
    # gtta.server lives behind the `enterprise` extra; skip where it is absent
    # rather than failing the base test job.
    pytest.importorskip("fastapi")
    from fastapi import HTTPException
    from fastapi.security import HTTPAuthorizationCredentials

    from gtta.server import require_api_key

    monkeypatch.delenv("GTTA_API_KEY", raising=False)
    with pytest.raises(HTTPException) as unconfigured:
        require_api_key(None)
    assert unconfigured.value.status_code == 503

    monkeypatch.setenv("GTTA_API_KEY", "correct-key")
    with pytest.raises(HTTPException) as missing:
        require_api_key(None)
    assert missing.value.status_code == 401

    with pytest.raises(HTTPException):
        require_api_key(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials="wrong")
        )

    ok = HTTPAuthorizationCredentials(scheme="Bearer", credentials="correct-key")
    assert require_api_key(ok) is None


def test_cli_does_not_use_shell_execution():
    from pathlib import Path

    import gtta.cli as cli_module

    source = Path(cli_module.__file__).read_text(encoding="utf-8")
    assert "os.system" not in source
    assert "subprocess.run" in source


def test_agent_result_exposes_failed_critic_state_without_claiming_pass():
    from gtta.agent import AnalystAgent

    agent = object.__new__(AnalystAgent)
    state = {
        "critique": "Missing source support",
        "iterations": 2,
        "validation_passed": False,
    }
    assert agent._route_critique(state) == "finish"
    assert state["validation_passed"] is False
