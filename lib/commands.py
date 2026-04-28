"""Comandos del agente"""

import os
import subprocess
from .ui import msg, input_, header, emoji, C, S
from . import chat_client
from .providers import get_active_provider

def chat_ai(prompt: str, contexto: str = ""):
    """Chat directo con IA"""
    proveedor = get_active_provider() or "ollama"
    
    full_prompt = contexto + "\n\n" + prompt if contexto else prompt
    
    msg("pensando", "El robot está pensando... 🤖")
    
    try:
        respuesta = chat_client.chat(full_prompt, proveedor)
        if respuesta:
            print(f"\n{respuesta}\n")
        else:
            msg("error", "No hubo respuesta del robot")
    except Exception as e:
        msg("error", f"Error: {e}")

def leer_archivo():
    """Leer archivo"""
    nombre = input_("Archivo a leer: ")
    if not nombre:
        msg("error", "Nombre de archivo requerido")
        return

    try:
        with open(nombre, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        msg("error", f"Archivo no encontrado: {nombre}")
        return
    except Exception as e:
        msg("error", f"Error: {e}")
        return

    print(f"\n{C.YELLOW}--- {nombre} ---{S.RESET_ALL}")
    print(contenido[:2000] + ("..." if len(contenido) > 2000 else ""))
    
    ask = input_(f"{C.CYAN}¿Analizar con IA? (s/n): {S.RESET_ALL}").lower()
    if ask == "s":
        pregunta = input_("Tu pregunta: ").strip()
        if pregunta:
            contexto = f"File:\n{contenido[:3000]}\n\nQuestion:"
            chat_ai(pregunta, contexto)

def editar_archivo():
    """Editar archivo"""
    nombre = input_("Archivo a editar: ")
    if not nombre:
        msg("error", "Nombre de archivo requerido")
        return

    try:
        with open(nombre, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        msg("error", f"Archivo no encontrado: {nombre}")
        return
    except Exception as e:
        msg("error", f"Error: {e}")
        return

    print(f"\n{C.YELLOW}Contenido actual ({len(contenido)} chars):{S.RESET_ALL}")
    print(contenido[:500] + ("..." if len(contenido) > 500 else ""))
    
    instruccion = input_(f"{C.CYAN}¿Qué quieres cambiar?: {S.RESET_ALL}").strip()
    if not instruccion:
        msg("error", "Instrucción requerida")
        return

    msg("pensando", "El robot está escribiendo... ✏️")
    
    contexto = f"Original file:\n{contenido[:3000]}\n\nInstruction: {instruccion}\n\nReturn only the new file content:"
    
    proveedor = get_active_provider() or "ollama"
    try:
        nuevo = chat_client.chat(contexto, proveedor)
        if nuevo:
            try:
                with open(nombre, "w", encoding="utf-8") as f:
                    f.write(nuevo)
                msg("ok", f"Archivo {nombre} actualizado")
            except Exception as e:
                msg("error", f"Error al guardar: {e}")
        else:
            msg("error", "No hubo respuesta")
    except Exception as e:
        msg("error", f"Error: {e}")

def instalar_deps():
    """Instalar dependencias"""
    if os.path.exists("package.json"):
        msg("info", "Proyecto Node.js detectado")
        msg("info", "Ejecutando npm install...")
        try:
            result = subprocess.run(["npm", "install"], capture_output=True, text=True)
            if result.returncode == 0:
                msg("ok", "Dependencias instaladas")
            else:
                msg("error", f"npm falló: {result.stderr}")
        except FileNotFoundError:
            msg("error", "npm no encontrado")
        return

    if os.path.exists("requirements.txt"):
        msg("info", "Proyecto Python detectado")
        msg("info", "Ejecutando pip install -r requirements.txt...")
        try:
            result = subprocess.run(
                ["pip", "install", "-r", "requirements.txt"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                msg("ok", "Dependencias instaladas")
            else:
                msg("error", f"pip falló: {result.stderr}")
        except FileNotFoundError:
            msg("error", "pip no encontrado")
        return

    msg("error", "No se detectó proyecto (package.json, requirements.txt, pyproject.toml)")

def depurar():
    """Debug de errores"""
    msg("info", "Pega el mensaje de error o describe el problema:")
    print("(Presiona Enter dos veces para enviar)")
    lineas = []
    while True:
        try:
            linea = input()
            if linea == "" and lineas:
                break
            lineas.append(linea)
        except EOFError:
            break
    
    error_msg = "\n".join(lineas).strip()
    if not error_msg:
        msg("error", "No hay mensaje de error")
        return

    msg("pensando", "El robot está analizando... 🔍")
    
    proveedor = get_active_provider() or "ollama"
    contexto = f"Error:\n{error_msg}\n\nAnalyze and suggest a fix:"
    
    try:
        solucion = chat_client.chat(contexto, proveedor)
        if solucion:
            header("Sugerencia de solución")
            print(solucion)
    except Exception as e:
        msg("error", f"Error: {e}")