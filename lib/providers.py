"""Proveedor de LLM con auto-deteccion"""

import os
import requests
from typing import Optional

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

class Provider:
    def __init__(self, name, status = "x"):
        self.name = name
        self.status = status
    
    def __str__(self):
        return self.status + " " + self.name

def check_ollama():
    try:
        resp = requests.get(OLLAMA_URL + "/api/tags", timeout=3)
        return resp.status_code == 200
    except:
        return False

def check_openai():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return False
    try:
        resp = requests.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": "Bearer " + key},
            timeout=5
        )
        return resp.status_code == 200
    except:
        return False

def check_anthropic():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return False
    try:
        resp = requests.get(
            "https://api.anthropic.com/v1/models",
            headers={"x-api-key": key, "anthropic-version": "2023-06-01"},
            timeout=5
        )
        return resp.status_code in (200, 201)
    except:
        return False

def check_openrouter():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        return False
    try:
        resp = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": "Bearer " + key},
            timeout=5
        )
        return resp.status_code == 200
    except:
        return False

def check_nvidia():
    key = os.environ.get("NVIDIA_API_KEY")
    if not key:
        return False
    try:
        resp = requests.get(
            "https://integrate.api.nvidia.com/v1/models",
            headers={"Authorization": "Bearer " + key},
            timeout=5
        )
        return resp.status_code == 200
    except:
        return False

def auto_detect():
    providers = []
    
    if check_ollama():
        providers.append(Provider("Ollama", "*"))
    else:
        providers.append(Provider("Ollama", " "))
    
    if check_openai():
        providers.append(Provider("OpenAI", "*"))
    else:
        providers.append(Provider("OpenAI", " "))
    
    if check_anthropic():
        providers.append(Provider("Anthropic", "*"))
    else:
        providers.append(Provider("Anthropic", " "))
    
    if check_openrouter():
        providers.append(Provider("OpenRouter", "*"))
    else:
        providers.append(Provider("OpenRouter", " "))
    
    if check_nvidia():
        providers.append(Provider("NVIDIA", "*"))
    else:
        providers.append(Provider("NVIDIA", " "))
    
    return providers

def get_active_provider():
    if check_ollama():
        return "ollama"
    if check_openai():
        return "openai"
    if check_anthropic():
        return "anthropic"
    if check_openrouter():
        return "openrouter"
    if check_nvidia():
        return "nvidia"
    return None