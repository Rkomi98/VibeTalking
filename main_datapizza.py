#!/usr/bin/env python3
"""
VibeTalking - Versione con DataPizzaAI
"""
import sys
import os
import asyncio
from pathlib import Path

# Fix crash XCB/ALSA in ambienti multi-thread
os.environ.setdefault("LIBXCB_ALLOW_SLOPPY_LOCK", "1")
os.environ.setdefault("QT_X11_NO_MITSHM", "1")
os.environ.setdefault("ALSA_PCM_CARD", "default")
os.environ.setdefault("ALSA_PCM_DEVICE", "0")

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    from tkinter.font import Font
except ImportError:
    print("❌ Tkinter non disponibile")
    sys.exit(1)

from src.config import Config
from src.audio import AudioRecorder
from src.ai.datapizza_analyzer import DataPizzaAudioAnalyzer


class DataPizzaMainWindow:
    """Finestra principale per VibeTalking con DataPizza"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎤 VibeTalking - DataPizza Edition")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        # Componenti
        self.recorder = AudioRecorder()
        self.analyzer = DataPizzaAudioAnalyzer()
        
        # Stato
        self.is_recording = False
        self.current_recording_file = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        # Font personalizzati
        title_font = Font(family="Arial", size=16, weight="bold")
        button_font = Font(family="Arial", size=12, weight="bold")
        
        # Titolo
        title_label = tk.Label(
            self.root,
            text="🎤 VibeTalking - DataPizza Edition",
            font=title_font,
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Stato analyzer
        analyzer_info = "🔧 DataPizza + Gemini 2.0 Flash" if not self.analyzer.demo_mode else "🔧 DataPizza Demo Mode"
        status_label = tk.Label(
            self.root,
            text=analyzer_info,
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        status_label.pack(pady=5)
        
        # Frame per i controlli
        controls_frame = tk.Frame(self.root, bg='#2c3e50')
        controls_frame.pack(pady=20)
        
        # Pulsante registrazione
        self.record_button = tk.Button(
            controls_frame,
            text="🎤 Inizia Registrazione",
            font=button_font,
            bg='#27ae60',
            fg='white',
            activebackground='#2ecc71',
            activeforeground='white',
            width=20,
            height=2,
            command=self.toggle_recording
        )
        self.record_button.pack(side=tk.LEFT, padx=10)
        
        # Pulsante analisi
        self.analyze_button = tk.Button(
            controls_frame,
            text="🔍 Analizza Audio",
            font=button_font,
            bg='#3498db',
            fg='white',
            activebackground='#5dade2',
            activeforeground='white',
            width=20,
            height=2,
            command=self.analyze_audio,
            state=tk.DISABLED
        )
        self.analyze_button.pack(side=tk.LEFT, padx=10)
        
        # Indicatore di stato
        self.status_var = tk.StringVar(value="✅ Pronto per registrare")
        status_indicator = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 12),
            bg='#2c3e50',
            fg='#2ecc71'
        )
        status_indicator.pack(pady=10)
        
        # Area risultati
        results_label = tk.Label(
            self.root,
            text="📋 Risultati Analisi",
            font=("Arial", 14, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        results_label.pack(pady=(20, 10))
        
        # Text area per i risultati
        self.results_text = scrolledtext.ScrolledText(
            self.root,
            width=90,
            height=20,
            font=("Consolas", 10),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='white',
            selectbackground='#5dade2'
        )
        self.results_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text="Powered by DataPizzaAI & Gemini 2.0 Flash",
            font=("Arial", 8),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        footer_label.pack(side=tk.BOTTOM, pady=5)
    
    def toggle_recording(self):
        """Avvia o ferma la registrazione"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Avvia la registrazione"""
        try:
            self.current_recording_file = self.recorder.start_recording()
            self.is_recording = True
            
            # Aggiorna UI
            self.record_button.config(
                text="⏹️ Ferma Registrazione",
                bg='#e74c3c',
                activebackground='#c0392b'
            )
            self.analyze_button.config(state=tk.DISABLED)
            self.status_var.set("🔴 Registrazione in corso...")
            
            print(f"🎤 Registrazione avviata: {self.current_recording_file}")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'avvio della registrazione: {e}")
    
    def stop_recording(self):
        """Ferma la registrazione"""
        try:
            if self.recorder.is_recording:
                self.recorder.stop_recording()
            
            self.is_recording = False
            
            # Aggiorna UI
            self.record_button.config(
                text="🎤 Inizia Registrazione",
                bg='#27ae60',
                activebackground='#2ecc71'
            )
            self.analyze_button.config(state=tk.NORMAL)
            self.status_var.set("✅ Registrazione completata - Pronto per analisi")
            
            print(f"⏹️ Registrazione fermata: {self.current_recording_file}")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel fermare la registrazione: {e}")
    
    def analyze_audio(self):
        """Analizza l'ultimo audio registrato"""
        if not self.current_recording_file:
            messagebox.showwarning("Attenzione", "Nessun file audio da analizzare")
            return
        
        # Disabilita i controlli durante l'analisi
        self.record_button.config(state=tk.DISABLED)
        self.analyze_button.config(state=tk.DISABLED)
        self.status_var.set("🔄 Analisi in corso con DataPizza...")
        
        # Avvia l'analisi in un thread separato
        import threading
        analysis_thread = threading.Thread(target=self.run_analysis_sync)
        analysis_thread.daemon = True
        analysis_thread.start()
    
    def run_analysis_sync(self):
        """Esegue l'analisi in modo sincrono per threading"""
        try:
            # Esegui l'analisi asincrona in un nuovo loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            results = loop.run_until_complete(
                self.analyzer.analyze_audio_file(self.current_recording_file)
            )
            
            # Salva i risultati
            output_file = self.analyzer.save_analysis_results(results)
            
            # Aggiorna UI nel thread principale
            self.root.after(0, lambda: self.display_results(results, output_file))
            self.root.after(0, lambda: self.status_var.set("✅ Analisi completata!"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Errore", f"Errore nell'analisi: {e}"))
            self.root.after(0, lambda: self.status_var.set("❌ Errore nell'analisi"))
        
        finally:
            # Riabilita i controlli nel thread principale
            self.root.after(0, lambda: self.record_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.analyze_button.config(state=tk.NORMAL))
    
    def display_results(self, results, output_file):
        """Mostra i risultati nell'area di testo"""
        self.results_text.delete(1.0, tk.END)
        
        # Formatta i risultati
        display_text = f"""
🎯 ANALISI DATAPIZZA COMPLETATA
{'='*50}

📁 File Audio: {results.get('file_path', 'N/A')}
💾 Risultati salvati in: {output_file}
🔧 Analyzer: {results.get('analyzer', 'N/A')}
⏰ Timestamp: {results.get('timestamp', 'N/A')}

📝 TRASCRIZIONE:
{'-'*30}
{results.get('transcription', 'N/A')}

🎭 ANALISI DEL TONO:
{'-'*30}
Tono principale: {results.get('tone_analysis', {}).get('tono_principale', 'N/A')}
Intensità: {results.get('tone_analysis', {}).get('intensità', 'N/A')}
Confidenza: {results.get('tone_analysis', {}).get('confidenza', 'N/A')}%
Descrizione: {results.get('tone_analysis', {}).get('descrizione', 'N/A')}

Emozioni secondarie: {', '.join(results.get('tone_analysis', {}).get('emozioni_secondarie', []))}

Suggerimenti:
{chr(10).join('• ' + s for s in results.get('tone_analysis', {}).get('suggerimenti', []))}

📋 RIASSUNTO:
{'-'*30}
{results.get('summary', 'N/A')}

{'='*50}
🎉 Analisi completata con DataPizzaAI!
        """
        
        self.results_text.insert(1.0, display_text.strip())
    
    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()


def main():
    """Funzione principale"""
    print("🎤 Avvio VibeTalking DataPizza Edition...")
    
    try:
        # Verifica configurazione
        Config.validate_config()
        print("✅ Configurazione validata")
        
        # Crea e avvia l'applicazione
        app = DataPizzaMainWindow()
        
        print("🚀 Applicazione DataPizza avviata!")
        print(f"📁 Directory output: {Config.OUTPUT_DIR}")
        
        app.run()
        
    except Exception as e:
        print(f"❌ Errore nell'avvio: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
