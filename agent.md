# Agent Documentation

## Overview

Mini Agente CLI is an AI-powered programming assistant that runs locally using Ollama and the Qwen3-Coder model.

## Architecture

### Core Components

| Component | File | Description |
|-----------|------|-------------|
| Entry Point | `agente.py` | Main CLI loop and menu |
| Commands | `lib/commands.py` | User command implementations |
| Ollama Client | `lib/ollama_client.py` | API client for Ollama |
| UI | `lib/ui.py` | Terminal output helpers |

### Dependencies

- `colorama` - Terminal colors
- `requests` - HTTP client (for Ollama API)
- `ollama` - Python Ollama SDK (optional)
- `inquirer` - Interactive prompts

## Development

### Adding New Commands

1. Add function to `lib/commands.py`:

```python
def my_command():
    """Description"""
    info("Running my command...")
    # implementation
```

2. Add to MENU in `agente.py`:

```python
("My Command", my_command),
```

### Ollama Integration

The client connects to `http://localhost:11434/api/chat` using the `qwen3-coder:7b` model by default.

To change the model, edit `lib/ollama_client.py`:

```python
MODEL = "qwen3-coder:7b"  # or another model
```

### System Prompts

The default system prompt is defined in `lib/ollama_client.py`:

```python
SYSTEM_PROMPT = (
    "You are a CLI programming assistant. "
    "Be concise. "
    "If modifying code, return ONLY the final content without markdown."
)
```

## Workflows

| Workflow | File | Trigger |
|----------|------|---------|
| Test | `test.yml` | Push/PR to main |
| Dependencies | `dep.yml` | Weekly or manual |

## Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python agente.py
```

### Production

```bash
# Make executable
chmod +x agente.py

# Run directly
./agente.py
```

Or install as a package with a setup script.

## Configuration

Environment variables can be used to override defaults:

```python
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen3-coder:7b")
```

## Troubleshooting

### Cannot connect to Ollama

```bash
# Start Ollama
ollama serve

# Pull model if needed
ollama pull qwen3-coder:7b
```

### Import errors

```bash
pip install -r requirements.txt
```

## License

MIT