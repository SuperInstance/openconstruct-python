"""Module registry for browsing available modules."""

import uuid
from typing import List, Optional

from openconstruct.types import ModuleInfo


class ModuleRegistry:
    """Registry of available OpenConstruct modules."""

    def __init__(self):
        """Initialize the module registry with sample modules."""
        self._modules = self._initialize_modules()

    def _initialize_modules(self) -> dict:
        """Initialize with sample modules."""
        return {
            "spectral-graph-core": ModuleInfo(
                id="spectral-graph-core",
                name="Spectral Graph Core",
                domain="math",
                description="Core spectral graph theory operations and algorithms",
                version="1.0.0",
                dependencies=[],
                requires_agent_capabilities=["computation"],
            ),
            "plato-room": ModuleInfo(
                id="plato-room",
                name="Plato Room",
                domain="collaboration",
                description="Virtual collaboration space for agent discussions",
                version="0.9.0",
                dependencies=["spectral-graph-core"],
                requires_agent_capabilities=["communication"],
            ),
            "tensor-flow": ModuleInfo(
                id="tensor-flow",
                name="Tensor Flow Operations",
                domain="math",
                description="Advanced tensor manipulation and operations",
                version="2.1.0",
                dependencies=[],
                requires_agent_capabilities=["computation"],
            ),
            "memory-bank": ModuleInfo(
                id="memory-bank",
                name="Memory Bank",
                domain="storage",
                description="Persistent memory storage for agents",
                version="1.2.0",
                dependencies=[],
                requires_agent_capabilities=["persistence"],
            ),
            "code-analyzer": ModuleInfo(
                id="code-analyzer",
                name="Code Analyzer",
                domain="analysis",
                description="Static code analysis and quality checks",
                version="0.8.0",
                dependencies=[],
                requires_agent_capabilities=["code_generation"],
            ),
            "web-crawler": ModuleInfo(
                id="web-crawler",
                name="Web Crawler",
                domain="web",
                description="Efficient web crawling and data extraction",
                version="1.5.0",
                dependencies=[],
                requires_agent_capabilities=["web_search"],
            ),
        }

    def list_modules(self, domain: Optional[str] = None) -> List[ModuleInfo]:
        """
        List all available modules, optionally filtered by domain.

        Args:
            domain: Optional domain filter (e.g., "math", "collaboration")

        Returns:
            List of ModuleInfo objects
        """
        modules = list(self._modules.values())
        if domain:
            modules = [m for m in modules if m.domain == domain]
        return modules

    def get_module(self, module_id: str) -> Optional[ModuleInfo]:
        """
        Get a specific module by ID.

        Args:
            module_id: The module identifier

        Returns:
            ModuleInfo if found, None otherwise
        """
        return self._modules.get(module_id)

    def module_exists(self, module_id: str) -> bool:
        """
        Check if a module exists.

        Args:
            module_id: The module identifier

        Returns:
            True if module exists, False otherwise
        """
        return module_id in self._modules