import requests
from .ui import info, error

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3-coder:7b"
TIMEOUT = 180

def chat(prompt, system_prompt=None, verbose=False):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        if verbose:
            info(f"Querying {MODEL}...")
        
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "messages": messages, "stream": False},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
    
    except requests.exceptions.ConnectionError:
        error("Cannot connect to Ollama. Is it running?")
        return None
    except requests.exceptions.Timeout:
        error("Timeout")
        return None
    except Exception as e:
        error(f"Error: {e}")
        return None

SYSTEM_PROMPT = (
    "You are a CLI programming assistant. "
    "Be concise. "
    "If modifying code, return ONLY the final content without markdown."
)