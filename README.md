# OpenConstruct Python

Python thin client for OpenConstruct — an agent can use it to onboard into the SuperInstance ecosystem.

## Installation

```bash
pip install openconstruct
```

## Quick Start

```python
from openconstruct import OpenConstructClient, AgentIdentity

# Create and start a client
client = OpenConstructClient()
client.start()

# Declare your agent
identity = AgentIdentity(
    name="my-agent",
    model="claude-4",
    capabilities=["code_generation", "web_search", "file_ops"],
    tools=["exec", "read", "write"]
)
client.declare_agent(identity)

# Browse and select modules
modules = client.list_modules(domain="math")
client.select_modules(["spectral-graph-core", "plato-room"])

# Choose interfaces
client.choose_interface(["cli", "api"])

# Generate configuration
config = client.generate_config()
print(config)
```

## Development

Install in development mode:

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT