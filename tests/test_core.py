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
