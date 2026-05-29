"""Data types for OpenConstruct."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentIdentity:
    """Agent self-declaration for onboarding."""

    name: str
    model: str
    capabilities: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    description: Optional[str] = None
    version: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert identity to dictionary."""
        return {
            "name": self.name,
            "model": self.model,
            "capabilities": self.capabilities,
            "tools": self.tools,
            "description": self.description,
            "version": self.version,
        }


@dataclass
class ModuleInfo:
    """Information about an available module."""

    id: str
    name: str
    domain: str
    description: str
    version: str
    dependencies: List[str] = field(default_factory=list)
    requires_agent_capabilities: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert module info to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "domain": self.domain,
            "description": self.description,
            "version": self.version,
            "dependencies": self.dependencies,
            "requires_agent_capabilities": self.requires_agent_capabilities,
        }


@dataclass
class OnboardingConfig:
    """Final onboarding configuration output."""

    session_id: str
    agent: Dict[str, Any]
    selected_modules: List[Dict[str, Any]]
    selected_interfaces: List[str]
    workspace: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "session_id": self.session_id,
            "agent": self.agent,
            "selected_modules": self.selected_modules,
            "selected_interfaces": self.selected_interfaces,
            "workspace": self.workspace,
            "created_at": self.created_at,
        }