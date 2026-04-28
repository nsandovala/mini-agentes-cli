#!/usr/bin/env python3
"""Mini Agente CLI v1.02 - Chat directo con IA"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"

from lib.ui import banner, msg, input_, header, separator, mostrar_comandos
from lib.providers import auto_detect, get_active_provider
from lib import chat_client

HISTORY = []
PROVEEDOR_ACTIVO = None

def mostrar_proveedores():
    providers = auto_detect()
    header("Proveedores disponibles")
    for p in providers:
        print("  " + str(p))
    print()

def mostrar_ayuda():
    print("")
    print("====================================================")
    print("  Mini Agente CLI v1.02 - Comandos")
    print("====================================================")
    print("")
    print("Comandos:")
    print("  /help       - Ver esta ayuda")
    print("  /clear     - Limpiar historial")
    print("  /proveedor - Ver proveedores disponibles")
    print("  /model    - Cambiar modelo")
    print("  /exit      - Salir")
    print("")
    print("Atajos:")
    print("  !q <pregunta> - Pregunta rapida")
    print("  !e <archivo>  - Editar archivo")
    print("  !r <archivo>  - Leer archivo")
    print("")
    print("Tips:")
    print("  - Escribe directamente tu pregunta")
    print("  - En espanol funciona bien")
    print("  - El robot te explica paso a paso")

def procesar_comando(cmd):
    cmd = cmd.lower().strip()
    
    if cmd in ("/help", "/ayuda", "ayuda", "help"):
        mostrar_ayuda()
        return True
    
    if cmd in ("/clear", "/limpiar", "clear"):
        global HISTORY
        HISTORY = []
        msg("ok", "Historial limpiado!")
        return True
    
    if cmd in ("/proveedor", "/providers", "proveedor"):
        mostrar_proveedores()
        return True
    
    if cmd in ("/model", "/modelo"):
        msg("info", "Selecciona proveedor:")
        mostrar_proveedores()
        return True
    
    if cmd in ("/exit", "/salir", "salir", "exit", "quit"):
        print("")
        print("[i] Hasta luego!")
        return False
    
    if cmd in ("/status", "status"):
        banner()
        mostrar_proveedores()
        return True
    
    return False

def chat(prompt):
    global HISTORY, PROVEEDOR_ACTIVO
    
    if not PROVEEDOR_ACTIVO:
        PROVEEDOR_ACTIVO = get_active_provider()
    
    if not PROVEEDOR_ACTIVO:
        msg("error", "Sin proveedor activo!")
        print("[i] Asegurate de tener:")
        print("  - Ollama corriendo")
        print("  - OPENAI_API_KEY en entorno")
        print("  - ANTHROPIC_API_KEY en entorno")
        return
    
    HISTORY.append({"role": "user", "content": prompt})
    
    msg("pensando", "El robot esta pensando...")
    
    try:
        respuesta = chat_client.chat(prompt, PROVEEDOR_ACTIVO, HISTORY)
        
        if respuesta:
            HISTORY.append({"role": "assistant", "content": respuesta})
            header("Respuesta")
            print("")
            print(respuesta)
            print("")
        else:
            msg("error", "No hubo respuesta")
            
    except Exception as e:
        msg("error", "Error: " + str(e))

def main():
    global PROVEEDOR_ACTIVO
    
    banner()
    
    PROVEEDOR_ACTIVO = get_active_provider()
    
    if PROVEEDOR_ACTIVO:
        msg("ok", "Conectado a: " + PROVEEDOR_ACTIVO)
    else:
        msg("error", "Sin proveedor activo")
    
    print()
    mostrar_proveedores()
    mostrar_ayuda()
    
    while True:
        try:
            prompt = input_("")
            
            if not prompt:
                continue
            
            if prompt.startswith("/"):
                if not procesar_comando(prompt):
                    break
                continue
            
            if prompt.startswith("!"):
                parte = prompt.split(None, 1)
                cmd = parte[0]
                arg = parte[1] if len(parte) > 1 else ""
                
                if cmd == "!q":
                    if not arg:
                        arg = input_("Tu pregunta: ")
                    if arg:
                        chat(arg)
                continue
            
            chat(prompt)
            
        except KeyboardInterrupt:
            print("")
            print("")
            print("[i] Hasta luego!")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()