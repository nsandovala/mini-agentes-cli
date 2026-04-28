# Mini Agente CLI

A powerful CLI programming assistant powered by [Ollama](https://github.com/ollama/ollama) and Qwen3-Coder.

## Features

- **File Analysis** - Read and analyze any file with AI
- **Code Editing** - Modify files using natural language instructions
- **Dependency Management** - Install npm/pip dependencies automatically
- **Debug Helper** - Paste error messages and get AI-powered solutions
- **Script Runner** - Execute npm scripts from package.json

## Requirements

- Python 3.8+
- [Ollama](https://ollama.ai) installed with `qwen3-coder:7b` model

```bash
ollama pull qwen3-coder:7b
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python agente.py
```

### Menu Options

1. **Read file** - Read a file and optionally analyze it with AI
2. **Edit file** - Edit a file using natural language instructions
3. **Install deps** - Install dependencies (npm/pip)
4. **Run script** - Execute npm scripts from package.json
5. **Search files** - Find files by extension pattern
6. **Debug** - Paste error messages for AI analysis

### Configuration

Edit `lib/ollama_client.py` to customize:

```python
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3-coder:7b"
TIMEOUT = 180
```

## Architecture

```
agente.py         # Main CLI entry point
lib/
  commands.py    # User commands implementation
  ui.py          # UI helpers (colors, prompts)
  ollama_client.py # Ollama API client
```

## Tech Stack

- **Python 3.8+**
- [ollama](https://pypi.org/project/ollama/) - Ollama Python SDK
- [colorama](https://pypi.org/project/colorama/) - Terminal colors
- [inquirer](https://pypi.org/project/inquirer/) - Interactive prompts

## License

MIT