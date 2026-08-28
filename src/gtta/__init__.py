"""Global Think Tank Analyst Python Package."""
__version__ = "1.4.0"

# Expose key components if their dependencies are met
try:
    from .langchain import get_system_prompt
except ImportError:
    pass

try:
    from .llamaindex import get_system_message, get_chat_template
except ImportError:
    pass

try:
    from .agent import AnalystAgent
except ImportError:
    pass

try:
    from .economics import calculate_unit_economics, calculate_cost
    from .knowledge import lookup_regional_knowledge
except ImportError:
    pass
