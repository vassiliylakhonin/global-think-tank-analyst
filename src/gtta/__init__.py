"""Global Think Tank Analyst — strategic-risk memo method and developer tools."""

from importlib.metadata import PackageNotFoundError, version as _version

# Single source of truth: the installed distribution. A hand-maintained literal
# here drifted to 1.4.0 while pyproject.toml moved on, so `gtta.__version__`
# reported a version that no longer matched the code it shipped with.
try:
    __version__ = _version("global-think-tank-analyst")
except PackageNotFoundError:  # running from a source tree without an install
    __version__ = "0+unknown"

from .skill import (
    SkillNotAvailableError,
    compose_prompt,
    get_skill_prompt,
    skill_path,
)

__all__ = [
    "__version__",
    "SkillNotAvailableError",
    "compose_prompt",
    "get_skill_prompt",
    "skill_path",
]

# Framework adapters and the agent pipeline live behind optional extras. They
# are re-exported when their dependencies are present and skipped otherwise;
# a missing extra is not an error, a missing method is.
try:
    from .langchain import get_system_prompt

    __all__.append("get_system_prompt")
except ImportError:  # pragma: no cover
    pass

try:
    from .llamaindex import get_chat_template, get_system_message

    __all__ += ["get_system_message", "get_chat_template"]
except ImportError:  # pragma: no cover
    pass

try:
    from .agent import AnalystAgent

    __all__.append("AnalystAgent")
except ImportError:  # pragma: no cover
    pass

try:
    from .economics import calculate_cost, calculate_unit_economics
    from .knowledge import lookup_regional_knowledge

    __all__ += ["calculate_unit_economics", "calculate_cost", "lookup_regional_knowledge"]
except ImportError:  # pragma: no cover
    pass
