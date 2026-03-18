import os
import subprocess
import requests
import sys

VERSION = "1.0.0"
# Jetzt mit deinem echten GitHub-Pfad:
GITHUB_USER = "flowtech12"
EXE_URL = f"https://github.com/{GITHUB_USER}/FlowCMD/raw/main/dist/FlowCMD.exe"
VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/FlowCMD/main/version.txt"

def run_update():
    print(">>> Update wird heruntergeladen...")
    r = requests.get(EXE_URL)
    with open("FlowCMD_new.exe", "wb") as f:
        f.write(r.content)
    
    # Erstellt eine temporäre Batch-Datei, um die EXE zu ersetzen
    with open("update.bat", "w") as f:
        f.write(f'@echo off\n')
        f.write(f'timeout /t 2 /nobreak > nul\n') # Wartet kurz, bis FlowCMD schließt
        f.write(f'del FlowCMD.exe\n')
        f.write(f'ren FlowCMD_new.exe FlowCMD.exe\n')
        f.write(f'start FlowCMD.exe\n')
        f.write(f'del "%~f0"\n') # Löscht sich selbst (die .bat) danach
    
    print(">>> Update bereit. FlowCMD startet neu...")
    os.startfile("update.bat")
    sys.exit()

def check_for_updates():
    try:
        r = requests.get(VERSION_URL, timeout=3)
        if r.status_code == 200:
            online_version = r.text.strip()
            if online_version > VERSION:
                return online_version
    except:
        pass
    return None

def main():
    print(f"--- FlowCMD v{VERSION} gestartet ---")
    new_v = check_for_updates()
    if new_v:
        print(f"[!] UPDATE VERFÜGBAR: Version {new_v}")
        wahl = input("Jetzt updaten? (j/n): ")
        if wahl.lower() == 'j':
            run_update()

    while True:
        cmd = input(f"\nFlow@CMD >> ").lower().strip()
        
        if cmd.startswith("mkdir "):
            name = cmd.split(" ", 1)[1]
            os.makedirs(name, exist_ok=True)
            print(f"Ordner '{name}' erstellt.")
            
        elif cmd.startswith("install "):
            app = cmd.split(" ", 1)[1]
            print(f"Windows bereitet {app} vor...")
            subprocess.run(["winget", "install", "-e", "--id", app])
            
        elif cmd == "exit":
            break
        else:
            print("Befehle: mkdir [Name], install [Programm], exit")

if __name__ == "__main__":
    main()