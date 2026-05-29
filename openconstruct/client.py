"""Main OpenConstruct client for agent onboarding."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from openconstruct.registry import ModuleRegistry
from openconstruct.types import AgentIdentity, ModuleInfo, OnboardingConfig


class OpenConstructClient:
    """Main client class for OpenConstruct onboarding."""

    def __init__(self):
        """Initialize the OpenConstruct client."""
        self._session_id: Optional[str] = None
        self._started = False
        self._identity: Optional[AgentIdentity] = None
        self._selected_modules: List[ModuleInfo] = []
        self._selected_interfaces: List[str] = []
        self._registry = ModuleRegistry()

    def start(self) -> str:
        """
        Start a new onboarding session.

        Returns:
            Session ID for the new session
        """
        self._session_id = str(uuid.uuid4())
        self._started = True
        self._identity = None
        self._selected_modules = []
        self._selected_interfaces = []
        return self._session_id

    def declare_agent(self, identity: AgentIdentity) -> None:
        """
        Declare agent identity.

        Args:
            identity: AgentIdentity object with agent details

        Raises:
            RuntimeError: If session not started
        """
        if not self._started:
            raise RuntimeError("Session not started. Call start() first.")
        self._identity = identity

    def list_modules(self, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available modules, optionally filtered by domain.

        Args:
            domain: Optional domain filter

        Returns:
            List of module dictionaries
        """
        modules = self._registry.list_modules(domain)
        return [m.to_dict() for m in modules]

    def select_modules(self, module_ids: List[str]) -> None:
        """
        Select modules for the agent.

        Args:
            module_ids: List of module IDs to select

        Raises:
            RuntimeError: If session not started
            ValueError: If any module ID is invalid
        """
        if not self._started:
            raise RuntimeError("Session not started. Call start() first.")

        for module_id in module_ids:
            if not self._registry.module_exists(module_id):
                raise ValueError(f"Module '{module_id}' not found")

        self._selected_modules = [
            self._registry.get_module(mid) for mid in module_ids if self._registry.get_module(mid)
        ]

    def choose_interface(self, interfaces: List[str]) -> None:
        """
        Choose interface types for the agent.

        Args:
            interfaces: List of interface types (e.g., ["cli", "api"])

        Raises:
            RuntimeError: If session not started
        """
        if not self._started:
            raise RuntimeError("Session not started. Call start() first.")
        self._selected_interfaces = interfaces

    def generate_config(self) -> Dict[str, Any]:
        """
        Generate the final onboarding configuration.

        Returns:
            Dictionary containing the complete onboarding configuration

        Raises:
            RuntimeError: If session not started or identity not declared
        """
        if not self._started:
            raise RuntimeError("Session not started. Call start() first.")

        if not self._identity:
            raise RuntimeError("Agent identity not declared. Call declare_agent() first.")

        config = OnboardingConfig(
            session_id=self._session_id,
            agent=self._identity.to_dict(),
            selected_modules=[m.to_dict() for m in self._selected_modules],
            selected_interfaces=self._selected_interfaces,
            workspace=self._build_workspace_config(),
            created_at=datetime.utcnow().isoformat() + "Z",
        )

        return config.to_dict()

    def _build_workspace_config(self) -> Dict[str, Any]:
        """
        Build workspace configuration based on selections.

        Returns:
            Dictionary with workspace configuration
        """
        workspace_config = {
            "agent_name": self._identity.name if self._identity else "",
            "modules": [m.id for m in self._selected_modules],
            "interfaces": self._selected_interfaces,
            "environment_variables": {
                "OPENCONSTRUCT_SESSION_ID": self._session_id or "",
            },
        }

        # Add module-specific configurations
        for module in self._selected_modules:
            workspace_config[f"module_{module.id}_config"] = {
                "version": module.version,
                "enabled": True,
            }

        return workspace_config

    @property
    def session_id(self) -> Optional[str]:
        """Get the current session ID."""
        return self._session_id

    @property
    def is_started(self) -> bool:
        """Check if a session is started."""
        return self._started

    @property
    def identity(self) -> Optional[AgentIdentity]:
        """Get the declared agent identity."""
        return self._identity