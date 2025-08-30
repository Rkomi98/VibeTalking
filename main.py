#!/usr/bin/env python3
"""
VibeTalking - Applicazione di Registrazione Audio con Analisi del Tono
"""
import sys
import os

# Fix crash XCB/ALSA in ambienti multi-thread
os.environ.setdefault("LIBXCB_ALLOW_SLOPPY_LOCK", "1")
os.environ.setdefault("QT_X11_NO_MITSHM", "1")
os.environ.setdefault("ALSA_PCM_CARD", "default")
os.environ.setdefault("ALSA_PCM_DEVICE", "0")

# Prova a usare GTK, altrimenti fallback a Tkinter
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from src.gui import MainWindow
    USE_GTK = True
    print("🖼️ Usando interfaccia GTK")
except Exception as e:
    print(f"⚠️ GTK non disponibile ({e}), uso Tkinter")
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    import threading
    import asyncio
    import math
    from pathlib import Path
    USE_GTK = False

from src.config import Config

# Se non abbiamo GTK, usa il main_demo direttamente
if not USE_GTK:
    print("🔄 Reindirizzamento a main_demo.py...")
    import subprocess
    import sys
    sys.exit(subprocess.call([sys.executable, 'main_demo.py']))

def main():
    """Funzione principale dell'applicazione"""
    print("🎤 Avvio VibeTalking...")
    
    try:
        # Verifica la configurazione
        Config.validate_config()
        print("✅ Configurazione validata")
        
        # Crea e mostra la finestra principale
        window = MainWindow()
        window.show_all()
        
        print("🚀 Applicazione avviata con successo!")
        print(f"📁 Directory output: {Config.OUTPUT_DIR}")
        
        # Avvia il loop principale di GTK
        Gtk.main()
        
    except ValueError as e:
        print(f"❌ Errore di configurazione: {e}")
        print("💡 Assicurati di aver creato il file .env con GOOGLE_API_KEY")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Errore nell'avvio dell'applicazione: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
