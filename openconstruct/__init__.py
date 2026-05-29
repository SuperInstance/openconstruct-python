"""OpenConstruct - Python thin client for SuperInstance ecosystem onboarding."""

from openconstruct.client import OpenConstructClient
from openconstruct.registry import ModuleRegistry
from openconstruct.types import AgentIdentity, ModuleInfo, OnboardingConfig

__version__ = "0.1.0"

__all__ = [
    "OpenConstructClient",
    "ModuleRegistry",
    "AgentIdentity",
    "ModuleInfo",
    "OnboardingConfig",
]