import pytest
from gtta.langchain import get_system_prompt
from gtta.llamaindex import get_system_message

def test_langchain_prompt():
    prompt = get_system_prompt(language="en")
    assert prompt is not None
    assert "Evidence mode" in prompt.content

def test_langchain_ru_prompt():
    prompt = get_system_prompt(language="ru")
    assert prompt is not None
    assert len(prompt.content) > 1000

def test_llamaindex_prompt():
    msg = get_system_message(language="en")
    assert msg.role.value == "system"
    assert "Evidence mode" in msg.content

def test_extra_instructions():
    prompt = get_system_prompt(extra_instructions="Focus on logistics.")
    assert "Focus on logistics." in prompt.content

def test_mcp_validation_tool():
    import asyncio
    from gtta.mcp_server import validate_memo_evidence
    
    # Missing tags
    result_fail = asyncio.run(validate_memo_evidence("Just some text."))
    assert "❌ Validation Failed" in result_fail
    assert "Missing 'Evidence mode:' declaration." in result_fail
    
    # Valid text
    valid_text = "Evidence mode: reasoning-only\n## Quick assessment\n[primary] Some fact.\n[inference] Some thought."
    result_pass = asyncio.run(validate_memo_evidence(valid_text))
    assert "✅ Validation passed" in result_pass

def test_unit_economics_calculation():
    from gtta.economics import calculate_unit_economics, calculate_cost
    
    cost = calculate_cost(1000, 500, model_name="deepseek-chat")
    assert cost > 0
    assert cost < 0.01
    
    econ = calculate_unit_economics(
        input_text="Sample input about sanctions on Middle Corridor." * 50,
        output_text="Sample output memo with executive summary and scenarios." * 100
    )
    assert econ["total_tokens"] > 0
    assert econ["gross_margin_pct"] > 95.0
    assert econ["cascading_savings_pct"] >= 0.0

def test_proprietary_knowledge_lookup():
    from gtta.knowledge import lookup_regional_knowledge
    
    res = lookup_regional_knowledge("What is the impact of Middle Corridor transport bottleneck in Aktau?")
    assert "PROPRIETARY DOMAIN REGISTER: MIDDLE_CORRIDOR" in res
    assert "Kazakhstan Temir Zholy" in res
    
    res_cbam = lookup_regional_knowledge("EU CBAM impact on Kazakh metals")
    assert "PROPRIETARY DOMAIN REGISTER: CBAM_KAZAKHSTAN" in res_cbam


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
    assert require_api_key(None) is None  # open demo while unset

    monkeypatch.setenv("GTTA_API_KEY", "correct-key")
    with pytest.raises(HTTPException) as missing:
        require_api_key(None)
    assert missing.value.status_code == 401

    with pytest.raises(HTTPException):
        require_api_key(HTTPAuthorizationCredentials(scheme="Bearer", credentials="wrong"))

    ok = HTTPAuthorizationCredentials(scheme="Bearer", credentials="correct-key")
    assert require_api_key(ok) is None
