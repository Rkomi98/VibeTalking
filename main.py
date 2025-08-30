#!/usr/bin/env python3
"""
VibeTalking - Applicazione di Registrazione Audio con Analisi del Tono
"""
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from src.gui import MainWindow
from src.config import Config

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
