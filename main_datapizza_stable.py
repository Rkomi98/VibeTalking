#!/usr/bin/env python3
"""
VibeTalking - Versione DataPizza Stabile (senza crash Linux)
"""
import sys
import os
import asyncio
from pathlib import Path
import threading

# Fix per Linux - variabili d'ambiente prima di importare GUI
os.environ.setdefault("LIBXCB_ALLOW_SLOPPY_LOCK", "1")
os.environ.setdefault("QT_X11_NO_MITSHM", "1")
os.environ.setdefault("ALSA_PCM_CARD", "0")
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


class VibeTalkingApp:
    """Applicazione VibeTalking stabile"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎤 VibeTalking - DataPizza Edition (Stable)")
        self.root.geometry("900x750")
        self.root.configure(bg='#1e1e1e')
        
        # Componenti
        self.recorder = AudioRecorder()
        self.analyzer = DataPizzaAudioAnalyzer()
        
        # Stato
        self.is_recording = False
        self.current_recording_file = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        # Stili
        style = ttk.Style()
        style.theme_use('clam')
        
        # Font
        title_font = Font(family="Arial", size=18, weight="bold")
        subtitle_font = Font(family="Arial", size=12)
        button_font = Font(family="Arial", size=11, weight="bold")
        
        # Header
        header_frame = tk.Frame(self.root, bg='#1e1e1e', pady=20)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="🎤 VibeTalking DataPizza Edition",
            font=title_font,
            bg='#1e1e1e',
            fg='#ffffff'
        )
        title_label.pack()
        
        # Stato analyzer
        analyzer_mode = "🔧 Gemini 2.0 Flash" if not self.analyzer.demo_mode else "🔧 Demo Mode"
        subtitle_label = tk.Label(
            header_frame,
            text=f"{analyzer_mode} • Audio Demo • Linux Stable",
            font=subtitle_font,
            bg='#1e1e1e',
            fg='#888888'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Controlli principali
        controls_frame = tk.Frame(self.root, bg='#1e1e1e')
        controls_frame.pack(pady=20)
        
        # Pulsante registrazione
        self.record_button = tk.Button(
            controls_frame,
            text="🎤 Inizia Registrazione",
            font=button_font,
            bg='#28a745',
            fg='white',
            activebackground='#34ce57',
            activeforeground='white',
            width=22,
            height=2,
            relief='flat',
            command=self.toggle_recording
        )
        self.record_button.pack(side=tk.LEFT, padx=10)
        
        # Pulsante analisi
        self.analyze_button = tk.Button(
            controls_frame,
            text="🔍 Analizza con DataPizza",
            font=button_font,
            bg='#007bff',
            fg='white',
            activebackground='#0056b3',
            activeforeground='white',
            width=22,
            height=2,
            relief='flat',
            command=self.start_analysis,
            state=tk.DISABLED
        )
        self.analyze_button.pack(side=tk.LEFT, padx=10)
        
        # Status
        self.status_var = tk.StringVar(value="✅ Pronto per registrare")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 12),
            bg='#1e1e1e',
            fg='#28a745'
        )
        status_label.pack(pady=10)
        
        # Area risultati
        results_frame = tk.Frame(self.root, bg='#1e1e1e')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        results_title = tk.Label(
            results_frame,
            text="📋 Risultati Analisi DataPizza",
            font=("Arial", 14, "bold"),
            bg='#1e1e1e',
            fg='#ffffff'
        )
        results_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Text area con scrollbar
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            width=100,
            height=25,
            font=("Consolas", 10),
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#ffffff',
            selectbackground='#007bff',
            selectforeground='#ffffff',
            wrap=tk.WORD
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text="Powered by DataPizzaAI & Gemini 2.0 Flash • Linux Stable Version",
            font=("Arial", 9),
            bg='#1e1e1e',
            fg='#666666'
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def toggle_recording(self):
        """Avvia/ferma registrazione"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Avvia registrazione"""
        try:
            self.current_recording_file = self.recorder.start_recording()
            if self.current_recording_file:
                self.is_recording = True
                
                # Aggiorna UI
                self.record_button.config(
                    text="⏹️ Ferma Registrazione",
                    bg='#dc3545',
                    activebackground='#c82333'
                )
                self.analyze_button.config(state=tk.DISABLED)
                self.status_var.set("🔴 Registrazione in corso...")
                
                print(f"🎤 Registrazione avviata: {self.current_recording_file}")
            else:
                messagebox.showerror("Errore", "Impossibile avviare la registrazione")
                
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'avvio della registrazione: {e}")
    
    def stop_recording(self):
        """Ferma registrazione"""
        try:
            if self.recorder.is_recording:
                saved_file = self.recorder.stop_recording()
                if saved_file:
                    self.current_recording_file = saved_file
            
            self.is_recording = False
            
            # Aggiorna UI
            self.record_button.config(
                text="🎤 Inizia Registrazione",
                bg='#28a745',
                activebackground='#34ce57'
            )
            self.analyze_button.config(state=tk.NORMAL)
            self.status_var.set("✅ Registrazione completata - Pronto per analisi")
            
            print(f"⏹️ Registrazione fermata: {self.current_recording_file}")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel fermare la registrazione: {e}")
    
    def start_analysis(self):
        """Avvia analisi in thread separato"""
        if not self.current_recording_file:
            messagebox.showwarning("Attenzione", "Nessun file audio da analizzare")
            return
        
        # Disabilita controlli
        self.record_button.config(state=tk.DISABLED)
        self.analyze_button.config(state=tk.DISABLED)
        self.status_var.set("🔄 Analisi DataPizza in corso...")
        
        # Avvia in thread
        analysis_thread = threading.Thread(target=self.run_analysis)
        analysis_thread.daemon = True
        analysis_thread.start()
    
    def run_analysis(self):
        """Esegue analisi in thread separato"""
        try:
            # Crea nuovo loop per il thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Esegui analisi
            results = loop.run_until_complete(
                self.analyzer.analyze_audio_file(self.current_recording_file)
            )
            
            # Salva risultati
            output_file = self.analyzer.save_analysis_results(results)
            
            # Aggiorna UI nel thread principale
            self.root.after(0, lambda: self.display_results(results, output_file))
            self.root.after(0, lambda: self.status_var.set("✅ Analisi DataPizza completata!"))
            
        except Exception as e:
            error_msg = f"Errore nell'analisi: {e}"
            self.root.after(0, lambda: messagebox.showerror("Errore", error_msg))
            self.root.after(0, lambda: self.status_var.set("❌ Errore nell'analisi"))
        
        finally:
            # Riabilita controlli
            self.root.after(0, lambda: self.record_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.analyze_button.config(state=tk.NORMAL))
    
    def display_results(self, results, output_file):
        """Mostra risultati nell'area di testo"""
        self.results_text.delete(1.0, tk.END)
        
        # Formatta risultati
        tone_analysis = results.get('tone_analysis', {})
        
        display_text = f"""
🎯 ANALISI DATAPIZZA COMPLETATA
{'='*60}

📁 File Audio: {results.get('file_path', 'N/A')}
💾 Risultati salvati: {output_file}
🔧 Analyzer: {results.get('analyzer', 'N/A')}
⏰ Timestamp: {results.get('timestamp', 'N/A')}

📝 TRASCRIZIONE:
{'-'*40}
{results.get('transcription', 'N/A')}

🎭 ANALISI DEL TONO:
{'-'*40}
• Tono principale: {tone_analysis.get('tono_principale', 'N/A')}
• Intensità: {tone_analysis.get('intensità', 'N/A')}
• Confidenza: {tone_analysis.get('confidenza', 'N/A')}%
• Descrizione: {tone_analysis.get('descrizione', 'N/A')}

Emozioni secondarie: {', '.join(tone_analysis.get('emozioni_secondarie', []))}

Suggerimenti:
{chr(10).join('• ' + s for s in tone_analysis.get('suggerimenti', []))}

📋 RIASSUNTO:
{'-'*40}
{results.get('summary', 'N/A')}

{'='*60}
🎉 Analisi completata con DataPizzaAI & Gemini 2.0 Flash!

💡 NOTA: Questa versione usa audio simulato per garantire stabilità su Linux.
   L'analisi AI è completamente funzionale con il modello Gemini.
        """
        
        self.results_text.insert(1.0, display_text.strip())
    
    def run(self):
        """Avvia l'applicazione"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Chiusura applicazione...")
        finally:
            self.recorder.cleanup()


def main():
    """Funzione principale"""
    print("🎤 Avvio VibeTalking DataPizza Stable...")
    
    try:
        # Verifica configurazione
        Config.validate_config()
        print("✅ Configurazione validata")
        
        # Crea e avvia app
        app = VibeTalkingApp()
        
        print("🚀 Applicazione DataPizza Stable avviata!")
        print(f"📁 Directory output: {Config.OUTPUT_DIR}")
        print("💡 Versione stabile per Linux - Audio simulato, AI reale")
        
        app.run()
        
    except Exception as e:
        print(f"❌ Errore critico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
