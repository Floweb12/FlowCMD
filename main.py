import requests
import os
import subprocess
import sys

# --- EINSTELLUNGEN ---
CURRENT_VERSION = "1.0.0"
# Dein GitHub-Pfad (Floweb12)
VERSION_URL = "https://raw.githubusercontent.com/Floweb12/FlowCMD/main/version.txt"
UPDATE_URL = "https://github.com/Floweb12/FlowCMD/releases/latest/download/setup.exe"

def check_for_updates():
    """Prüft online bei Floweb12 nach einer neuen Version."""
    print(f"[*] Suche nach Updates für FlowCMD (v{CURRENT_VERSION})...")
    try:
        response = requests.get(VERSION_URL, timeout=5)
        online_version = response.text.strip()

        if online_version != CURRENT_VERSION:
            print(f"\n[!] UPDATE VERFÜGBAR: Version {online_version} gefunden!")
            choice = input("Möchtest du das Update jetzt installieren? (j/n): ")
            if choice.lower() == 'j':
                download_update()
        else:
            print("[+] FlowCMD ist auf dem neuesten Stand.\n")
    except Exception as e:
        print(f"[-] Update-Server nicht erreichbar: {e}\n")

def download_update():
    """Lädt die neue setup.exe herunter und startet sie."""
    print("[*] Windows wird auf das Update vorbereitet...")
    try:
        r = requests.get(UPDATE_URL, stream=True)
        with open("setup_update.exe", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("[+] Download abgeschlossen. Installer startet...")
        subprocess.Popen(["setup_update.exe"])
        sys.exit(0) # Beendet FlowCMD für die Installation
    except Exception as e:
        print(f"[-] Fehler beim Download: {e}")

def main():
    """Die Hauptschleife deines Tools."""
    print("========================================")
    print(f"      FlowCMD v{CURRENT_VERSION} - Floweb12")
    print("   Tippe 'help' für Befehle oder 'exit'")
    print("========================================\n")

    while True:
        # Dein Prompt (Eingabezeile)
        cmd = input("FlowCMD > ").lower().strip()

        if cmd == "exit":
            print("Bis zum nächsten Mal, Flow!")
            break
        
        elif cmd == "help":
            print("\nVerfügbare Befehle:")
            print(" - help:  Zeigt diese Liste")
            print(" - info:  Infos über FlowCMD")
            print(" - cls:   Bildschirm leeren")
            print(" - exit:  Programm beenden\n")
        
        elif cmd == "info":
            print(f"\nFlowCMD Version: {CURRENT_VERSION}")
            print("Entwickler: Flow (Floweb12)")
            print("Status: Feiertags-Build (St. Josef)\n")
        
        elif cmd == "cls":
            os.system('cls' if os.name == 'nt' else 'clear')
        
        elif cmd == "":
            continue
            
        else:
            print(f"[-] Befehl '{cmd}' unbekannt. Tippe 'help' für Hilfe.")

# --- STARTPUNKT ---
if __name__ == "__main__":
    # 1. Update prüfen
    check_for_updates()
    
    # 2. Tool starten
    try:
        main()
    except KeyboardInterrupt:
        print("\nFlowCMD abgebrochen.")
        sys.exit(0)