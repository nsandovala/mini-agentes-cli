import os
import subprocess
from .ui import error, ok, info, header, input_
from . import ollama_client

def leer_archivo():
    nombre = input_("File: ")
    if not nombre:
        error("Filename required")
        return

    try:
        with open(nombre, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        error(f"File not found: {nombre}")
        return
    except Exception as e:
        error(f"Error: {e}")
        return

    print(f"\n--- {nombre} ---")
    print(contenido[:2000] + ("..." if len(contenido) > 2000 else ""))
    
    ask = input_("\nAnalyze with AI? (y/n): ").lower()
    if ask == "y":
        info("Analyzing...")
        pregunta = input_("Question: ").strip()
        if pregunta:
            respuesta = ollama_client.chat(
                f"File:\n{contenido}\n\nQuestion: {pregunta}",
                ollama_client.SYSTEM_PROMPT,
                verbose=True
            )
            if respuesta:
                header("Analysis")
                print(respuesta)

def editar_archivo():
    nombre = input_("File: ")
    if not nombre:
        error("Filename required")
        return

    try:
        with open(nombre, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        error(f"File not found: {nombre}")
        return
    except Exception as e:
        error(f"Error: {e}")
        return

    print(f"\nCurrent ({len(contenido)} chars):")
    print(contenido[:500] + ("..." if len(contenido) > 500 else ""))
    
    instruccion = input_("\nInstruction: ").strip()
    if not instruccion:
        error("Instruction required")
        return

    info("Generating...")
    nuevo = ollama_client.chat(
        f"Original file:\n{contenido}\n\nInstruction: {instruccion}\n\nReturn only the new file content:",
        ollama_client.SYSTEM_PROMPT,
        verbose=True
    )

    if nuevo:
        try:
            with open(nombre, "w", encoding="utf-8") as f:
                f.write(nuevo)
            ok(f"File {nombre} updated")
        except Exception as e:
            error(f"Save error: {e}")

def instalar_deps():
    if os.path.exists("package.json"):
        info("Node.js project detected")
        info("Running npm install...")
        try:
            result = subprocess.run(["npm", "install"], capture_output=True, text=True)
            if result.returncode == 0:
                ok("Dependencies installed")
            else:
                error(f"npm failed: {result.stderr}")
        except FileNotFoundError:
            error("npm not found")
        return

    if os.path.exists("requirements.txt"):
        info("Python project detected")
        info("Running pip install -r requirements.txt...")
        try:
            result = subprocess.run(
                ["pip", "install", "-r", "requirements.txt"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                ok("Dependencies installed")
            else:
                error(f"pip failed: {result.stderr}")
        except FileNotFoundError:
            error("pip not found")
        return

    if os.path.exists("pyproject.toml"):
        info("pyproject.toml detected")
        info("Running pip install -e . ...")
        try:
            result = subprocess.run(["pip", "install", "-e", "."], capture_output=True, text=True)
            if result.returncode == 0:
                ok("Package installed")
            else:
                error(f"pip failed: {result.stderr}")
        except Exception as e:
            error(f"Error: {e}")
        return

    error("No project detected (package.json, requirements.txt, pyproject.toml)")

def depurar():
    info("Paste error message or describe problem:")
    print("(Press Enter twice to send)")
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
        error("No error message")
        return

    info("Analyzing...")
    solucion = ollama_client.chat(
        f"Error:\n{error_msg}\n\nAnalyze and suggest a fix:",
        ollama_client.SYSTEM_PROMPT + " You are a debugging expert.",
        verbose=True
    )

    if solucion:
        header("Fix suggestion")
        print(solucion)