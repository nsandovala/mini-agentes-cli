#!/usr/bin/env python3
"""Mini Agente CLI - MVP con Qwen3-Coder"""
import subprocess
import json
import os
from lib.ui import error, ok, info, pedir_numero
from lib import commands

MENU = [
    ("Read file", commands.leer_archivo),
    ("Edit file", commands.editar_archivo),
    ("Install deps", commands.instalar_deps),
    ("Run script", None),
    ("Search files", None),
    ("Debug", commands.depurar),
]

def run_script():
    if not os.path.exists("package.json"):
        error("No package.json found")
        return
    
    try:
        with open("package.json") as f:
            scripts = json.load(f).get("scripts", {})
    except:
        error("Invalid package.json")
        return
    
    if not scripts:
        error("No scripts defined")
        return
    
    print("Available scripts:")
    for i, name in enumerate(scripts.keys(), 1):
        print(f"  {i}. {name}")
    
    sel = pedir_numero(1, len(scripts))
    script_name = list(scripts.keys())[sel - 1]
    
    info(f"Running npm run {script_name}...")
    result = subprocess.run(
        ["npm", "run", script_name],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.stderr:
        error(result.stderr)
    else:
        ok(f"Script {script_name} completed")

def search_files():
    patron = input("Pattern (e.g. *.js, *.py): ").strip()
    if not patron:
        error("Pattern required")
        return
    
    ext = patron.replace("*", "")
    encontrados = []
    
    for root, dirs, files in os.walk("."):
        if "node_modules" in root or ".git" in root:
            continue
        for f in files:
            if f.endswith(ext.replace(".", "")):
                encontrados.append(os.path.join(root, f))
    
    if encontrados:
        for f in encontrados[:20]:
            print(f"  {f}")
        if len(encontrados) > 20:
            print(f"  ... and {len(encontrados) - 20} more")
    else:
        error("No files found")

def mostrar_menu():
    print()
    print("=== MINI AGENTE ===")
    for i, (nombre, _) in enumerate(MENU, 1):
        print(f"  {i}. {nombre}")
    print(f"  {len(MENU) + 1}. Exit")

def main():
    while True:
        mostrar_menu()
        
        try:
            sel = pedir_numero(1, len(MENU) + 1)
        except (KeyboardInterrupt, EOFError):
            print("\n")
            break
        
        if sel == len(MENU) + 1:
            print("Bye!")
            break
        
        print()
        func = MENU[sel - 1][1]
        
        if func:
            try:
                func()
            except KeyboardInterrupt:
                error("Cancelled")
            except Exception as e:
                error(f"Error: {e}")
        elif sel == 4:
            run_script()
        elif sel == 5:
            search_files()
        else:
            error("Not implemented")

if __name__ == "__main__":
    main()