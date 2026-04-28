from colorama import init, Fore, Style

init(autoreset=True)

def error(txt):
    print(f"{Fore.RED}Error: {txt}{Style.RESET_ALL}")

def ok(txt):
    print(f"{Fore.GREEN}✓ {txt}{Style.RESET_ALL}")

def info(txt):
    print(f"{Fore.BLUE}>{txt}{Style.RESET_ALL}")

def header(txt):
    print(f"{Style.BRIGHT}{txt}{Style.RESET_ALL}")

def input_(txt):
    return input(f"{Style.BRIGHT}>{Style.RESET_ALL} {txt} ").strip()

def pedir_numero(min_val, max_val):
    while True:
        try:
            val = int(input(f"[{min_val}-{max_val}] "))
            if min_val <= val <= max_val:
                return val
        except ValueError:
            pass
        error(f"Invalid. Enter {min_val}-{max_val}")