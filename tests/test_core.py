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

@pytest.mark.asyncio
async def test_mcp_validation_tool():
    from gtta.mcp_server import validate_memo_evidence
    
    # Missing tags
    result_fail = await validate_memo_evidence("Just some text.")
    assert "❌ Validation Failed" in result_fail
    assert "Missing 'Evidence mode:' declaration." in result_fail
    
    # Valid text
    valid_text = "Evidence mode: reasoning-only\n## Quick assessment\n[primary] Some fact.\n[inference] Some thought."
    result_pass = await validate_memo_evidence(valid_text)
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
