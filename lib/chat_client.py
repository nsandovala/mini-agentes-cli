"""Cliente de chat con múltiples proveedores"""

import os
import json
import requests
from typing import Optional

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

SYSTEM_PROMPT = """Eres un asistente de programación educativo.
Explicas las cosas de forma sencilla, como un maestro paciente.
Usas ejemplos cuando hace falta. Usas emojis en tus respuestas."""

def chat_ollama(prompt: str, model: str = "qwen3-coder:7b", history: list = None, verbose: bool = True) -> Optional[str]:
    """Chat con Ollama local"""
    messages = []
    if history:
        messages.extend(history[-6:])  # último 6 mensajes
    messages.append({"role": "user", "content": prompt})
    
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": model, "messages": messages, "stream": False},
            timeout=180
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]
    except Exception as e:
        if verbose:
            print(f"Ollama error: {e}")
        return None

def chat_openai(prompt: str, model: str = "gpt-4o-mini", history: list = None, api_key: str = None, verbose: bool = True) -> Optional[str]:
    """Chat con OpenAI"""
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        if verbose:
            print("OpenAI: No API key")
        return None
    
    messages = []
    if history:
        messages.extend(history[-6:])
    messages.append({"role": "user", "content": prompt})
    
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={"model": model, "messages": messages},
            timeout=120
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        if verbose:
            print(f"OpenAI error: {e}")
        return None

def chat_anthropic(prompt: str, model: str = "claude-sonnet-4-20250514", history: list = None, api_key: str = None, verbose: bool = True) -> Optional[str]:
    """Chat con Anthropic"""
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        if verbose:
            print("Anthropic: No API key")
        return None
    
    messages = []
    if history:
        for h in history[-6:]:
            role = h.get("role", "user")
            if role == "assistant":
                role = "assistant"
            messages.append({"role": role, "content": h["content"]})
    messages.append({"role": "user", "content": prompt})
    
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={"model": model, "max_tokens": 4096, "messages": messages},
            timeout=120
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]
    except Exception as e:
        if verbose:
            print(f"Anthropic error: {e}")
        return None

def chat_openrouter(prompt: str, model: str = "openai/gpt-4o-mini", history: list = None, api_key: str = None, verbose: bool = True) -> Optional[str]:
    """Chat con OpenRouter"""
    key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        if verbose:
            print("OpenRouter: No API key")
        return None
    
    messages = []
    if history:
        messages.extend(history[-6:])
    messages.append({"role": "user", "content": prompt})
    
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={"model": model, "messages": messages},
            timeout=120
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        if verbose:
            print(f"OpenRouter error: {e}")
        return None

def chat_nvidia(prompt: str, model: str = "nvidia/llama-3.1-nemotron-70b-instruct", history: list = None, api_key: str = None, verbose: bool = True) -> Optional[str]:
    """Chat con NVIDIA AI Foundry"""
    key = api_key or os.environ.get("NVIDIA_API_KEY")
    if not key:
        if verbose:
            print("NVIDIA: No API key")
        return None
    
    messages = []
    if history:
        messages.extend(history[-6:])
    messages.append({"role": "user", "content": prompt})
    
    try:
        resp = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={"model": model, "messages": messages},
            timeout=120
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        if verbose:
            print(f"NVIDIA error: {e}")
        return None

MODELOS = {
    "ollama": ["qwen3-coder:7b", "codellama:7b", "mistral:7b"],
    "openai": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
    "anthropic": ["claude-sonnet-4-20250514", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
    "openrouter": ["openai/gpt-4o-mini", "anthropic/claude-3-haiku", "google/gemini-pro-1.5"],
    "nvidia": ["nvidia/llama-3.1-nemotron-70b-instruct", "nvidia/llama-3.1-nemotron-8b-instruct"],
}

def chat(prompt: str, provider: str = "ollama", history: list = None, model: str = None, verbose: bool = True) -> Optional[str]:
    """Función principal de chat - Routing según proveedor"""
    
    if not model:
        model = MODELOS.get(provider, ["gpt-4o-mini"])[0]
    
    if provider == "ollama":
        return chat_ollama(prompt, model, history, verbose)
    elif provider == "openai":
        return chat_openai(prompt, model, history, verbose=verbose)
    elif provider == "anthropic":
        return chat_anthropic(prompt, model, history, verbose=verbose)
    elif provider == "openrouter":
        return chat_openrouter(prompt, model, history, verbose=verbose)
    elif provider == "nvidia":
        return chat_nvidia(prompt, model, history, verbose=verbose)
    else:
        if verbose:
            print(f"Proveedor desconocido: {provider}")
        return None