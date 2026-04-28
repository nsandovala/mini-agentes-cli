"""UI simple sin emojis para compatibilidad Windows"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

def banner():
    print("")
    print("=====================================")
    print("  Mini Agente CLI - Coding con IA")
    print("  Aprende a programar!")
    print("=====================================")
    print("")

def msg(tipo, txt):
    if tipo == "info":
        print("[i] " + txt)
    elif tipo == "ok":
        print("[+] " + txt)
    elif tipo == "error":
        print("[!] " + txt)
    elif tipo == "ayuda":
        print("[?] " + txt)
    elif tipo == "pensando":
        print("[...] " + txt)
    else:
        print(txt)

def input_(txt):
    if txt:
        return input("> " + txt).strip()
    return input("> ").strip()

def header(txt):
    print("")
    print("--- " + txt + " ---")

def separator():
    print("-" * 40)

def mostrar_comandos():
    print("")
    print("Comandos:")
    print("  /help     - Ver ayuda")
    print("  /clear    - Limpiar")
    print("  /model    - Cambiar modelo")
    print("  /proveedor- Ver proveedores")
    print("  /exit     - Salir")
    print("")