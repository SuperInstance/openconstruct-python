# OpenConstruct Python — Thin Client for Agent Onboarding

Python client for [OpenConstruct](https://github.com/SuperInstance/OpenConstruct). Onboard agents into the SuperInstance ecosystem in under 10 lines.

## What This Gives You

- **5-phase onboarding** — `start()` → `declare_agent()` → `select_modules()` → `choose_interface()` → `generate_config()`
- **Module registry** — domain-filtered catalog of available modules
- **Pip-installable** — `pip install openconstruct`
- **Zero runtime dependencies** — pure Python, no native extensions

## Quick Start

```python
from openconstruct import OpenConstructClient, AgentIdentity

client = OpenConstructClient()
client.start()

identity = AgentIdentity(
    name="my-agent",
    model="claude-4",
    capabilities=["code_generation", "web_search", "file_ops"],
    tools=["exec", "read", "write"]
)
client.declare_agent(identity)

modules = client.list_modules(domain="math")
client.select_modules(["spectral-graph-core", "plato-room"])
client.choose_interface(["cli", "api"])

config = client.generate_config()
print(config)
```

## Installation

```bash
pip install openconstruct
```

## Testing

```bash
pip install -e ".[dev]"
pytest
```

## How It Fits

One of the [polyglot OpenConstruct bindings](https://github.com/SuperInstance/OpenConstruct). Used by [openconstruct-jupyter](https://github.com/SuperInstance/openconstruct-jupyter) for notebook integration. See [openconstruct-examples](https://github.com/SuperInstance/openconstruct-examples) for a Python onboarding walkthrough.

## License

MIT
