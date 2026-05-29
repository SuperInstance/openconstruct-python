"""Tests for OpenConstructClient."""

import pytest

from openconstruct import OpenConstructClient, AgentIdentity


class TestClientStart:
    """Tests for client start functionality."""

    def test_start_creates_session(self):
        """Test that start() creates a session with a valid ID."""
        client = OpenConstructClient()
        session_id = client.start()

        assert isinstance(session_id, str)
        assert len(session_id) > 0
        assert client.is_started
        assert client.session_id == session_id


class TestClientDeclareAgent:
    """Tests for agent declaration."""

    def test_declare_agent_stores_identity(self):
        """Test that declare_agent() stores the identity."""
        client = OpenConstructClient()
        client.start()

        identity = AgentIdentity(
            name="test-agent",
            model="gpt-4",
            capabilities=["test"],
            tools=["exec"]
        )
        client.declare_agent(identity)

        assert client.identity is not None
        assert client.identity.name == "test-agent"
        assert client.identity.model == "gpt-4"

    def test_declare_agent_fails_without_start(self):
        """Test that declare_agent() raises error without start()."""
        client = OpenConstructClient()
        identity = AgentIdentity(name="test", model="gpt-4")

        with pytest.raises(RuntimeError, match="Session not started"):
            client.declare_agent(identity)


class TestClientListModules:
    """Tests for module listing."""

    def test_list_modules_returns_list(self):
        """Test that list_modules() returns a list."""
        client = OpenConstructClient()
        client.start()

        modules = client.list_modules()

        assert isinstance(modules, list)
        assert len(modules) > 0
        assert all(isinstance(m, dict) for m in modules)

    def test_list_modules_filters_by_domain(self):
        """Test that list_modules(domain=X) filters correctly."""
        client = OpenConstructClient()
        client.start()

        math_modules = client.list_modules(domain="math")
        all_modules = client.list_modules()

        assert len(math_modules) < len(all_modules)
        assert all(m["domain"] == "math" for m in math_modules)

    def test_list_modules_with_unknown_domain(self):
        """Test that list_modules() with unknown domain returns empty list."""
        client = OpenConstructClient()
        client.start()

        modules = client.list_modules(domain="nonexistent")

        assert isinstance(modules, list)
        assert len(modules) == 0


class TestClientSelectModules:
    """Tests for module selection."""

    def test_select_modules_stores_selection(self):
        """Test that select_modules() stores the selection."""
        client = OpenConstructClient()
        client.start()
        client.declare_agent(AgentIdentity(name="test", model="gpt-4"))

        client.select_modules(["spectral-graph-core", "plato-room"])

        config = client.generate_config()
        assert len(config["selected_modules"]) == 2

    def test_select_modules_fails_without_start(self):
        """Test that select_modules() raises error without start()."""
        client = OpenConstructClient()

        with pytest.raises(RuntimeError, match="Session not started"):
            client.select_modules(["spectral-graph-core"])

    def test_select_modules_fails_with_invalid_module(self):
        """Test that select_modules() raises error with invalid module."""
        client = OpenConstructClient()
        client.start()

        with pytest.raises(ValueError, match="not found"):
            client.select_modules(["nonexistent-module"])

    def test_select_modules_with_mixed_valid_invalid(self):
        """Test that select_modules() fails with mix of valid and invalid modules."""
        client = OpenConstructClient()
        client.start()

        with pytest.raises(ValueError, match="not found"):
            client.select_modules(["spectral-graph-core", "invalid-module"])


class TestClientChooseInterface:
    """Tests for interface selection."""

    def test_choose_interface_stores_choice(self):
        """Test that choose_interface() stores the choice."""
        client = OpenConstructClient()
        client.start()
        client.declare_agent(AgentIdentity(name="test", model="gpt-4"))

        client.choose_interface(["cli", "api"])

        config = client.generate_config()
        assert config["selected_interfaces"] == ["cli", "api"]

    def test_choose_interface_fails_without_start(self):
        """Test that choose_interface() raises error without start()."""
        client = OpenConstructClient()

        with pytest.raises(RuntimeError, match="Session not started"):
            client.choose_interface(["cli"])


class TestClientGenerateConfig:
    """Tests for configuration generation."""

    def test_generate_config_produces_dict(self):
        """Test that generate_config() produces a dictionary."""
        client = OpenConstructClient()
        client.start()
        client.declare_agent(AgentIdentity(name="test", model="gpt-4"))

        config = client.generate_config()

        assert isinstance(config, dict)

    def test_generate_config_has_required_fields(self):
        """Test that generate_config() has all required fields."""
        client = OpenConstructClient()
        client.start()
        client.declare_agent(AgentIdentity(name="test", model="gpt-4"))

        config = client.generate_config()

        assert "session_id" in config
        assert "agent" in config
        assert "selected_modules" in config
        assert "selected_interfaces" in config
        assert "workspace" in config
        assert "created_at" in config

    def test_generate_config_fails_without_start(self):
        """Test that generate_config() raises error without start()."""
        client = OpenConstructClient()

        with pytest.raises(RuntimeError, match="Session not started"):
            client.generate_config()

    def test_generate_config_fails_without_identity(self):
        """Test that generate_config() raises error without identity."""
        client = OpenConstructClient()
        client.start()

        with pytest.raises(RuntimeError, match="Agent identity not declared"):
            client.generate_config()


class TestClientFullLifecycle:
    """Tests for the complete client lifecycle."""

    def test_full_lifecycle(self):
        """Test the complete onboarding flow."""
        client = OpenConstructClient()

        # Start session
        session_id = client.start()
        assert session_id is not None

        # Declare agent
        identity = AgentIdentity(
            name="my-agent",
            model="claude-4",
            capabilities=["code_generation", "web_search", "file_ops"],
            tools=["exec", "read", "write"]
        )
        client.declare_agent(identity)
        assert client.identity.name == "my-agent"

        # List and select modules
        modules = client.list_modules(domain="math")
        assert len(modules) > 0

        client.select_modules(["spectral-graph-core", "plato-room"])

        # Choose interfaces
        client.choose_interface(["cli", "api"])

        # Generate config
        config = client.generate_config()

        # Verify structure
        assert config["session_id"] == session_id
        assert config["agent"]["name"] == "my-agent"
        assert len(config["selected_modules"]) == 2
        assert config["selected_interfaces"] == ["cli", "api"]
        assert "workspace" in config
        assert config["created_at"] != ""

    def test_lifecycle_with_multiple_sessions(self):
        """Test that starting a new session resets state."""
        client = OpenConstructClient()

        # First session
        client.start()
        client.declare_agent(AgentIdentity(name="agent1", model="gpt-4"))
        session1_id = client.session_id

        # Second session
        client.start()
        client.declare_agent(AgentIdentity(name="agent2", model="claude-4"))
        session2_id = client.session_id

        assert session1_id != session2_id
        assert client.identity.name == "agent2"