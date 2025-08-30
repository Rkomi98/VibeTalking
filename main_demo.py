#!/usr/bin/env python3
"""
VibeTalking - Versione Demo con Tkinter
"""
import sys
import os

# Fix crash XCB/ALSA in ambienti multi-thread
os.environ.setdefault("LIBXCB_ALLOW_SLOPPY_LOCK", "1")
os.environ.setdefault("QT_X11_NO_MITSHM", "1")
os.environ.setdefault("ALSA_PCM_CARD", "default")
os.environ.setdefault("ALSA_PCM_DEVICE", "0")

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import asyncio
import math
from pathlib import Path

from src.audio import AudioRecorder
from src.ai import AudioAnalyzer
from src.config import Config

class ToneVisualizerTk(tk.Canvas):
    """Visualizzatore del tono con Tkinter"""
    
    def __init__(self, parent):
        super().__init__(parent, width=300, height=300, bg='black')
        
        self.current_tone = "neutrale"
        self.intensity = 0.5
        self.confidence = 0.5
        self.is_recording = False
        self.animation_step = 0
        
        # Colori per i toni
        self.tone_colors = {
            "entusiasta": "#FF9900",
            "felice": "#FFCC00", 
            "calmo": "#00BBFF",
            "neutrale": "#808080",
            "preoccupato": "#CC6600",
            "arrabbiato": "#FF3333",
            "triste": "#4D4DCC",
            "eccitato": "#FF00FF",
        }
        
        self.start_animation()
    
    def update_tone(self, tone_data):
        """Aggiorna il tono visualizzato"""
        if tone_data:
            self.current_tone = tone_data.get("tono_principale", "neutrale")
            
            intensity_map = {"bassa": 0.3, "media": 0.6, "alta": 0.9}
            self.intensity = intensity_map.get(tone_data.get("intensità", "media"), 0.6)
            self.confidence = tone_data.get("confidenza", 50) / 100.0
    
    def set_recording_state(self, is_recording):
        """Imposta lo stato di registrazione"""
        self.is_recording = is_recording
    
    def start_animation(self):
        """Avvia l'animazione"""
        self.animate()
    
    def animate(self):
        """Aggiorna l'animazione"""
        self.delete("all")
        
        center_x, center_y = 150, 150
        
        if self.is_recording:
            # Cerchio principale animato
            color = self.tone_colors.get(self.current_tone, "#808080")
            
            # Pulsazione basata sull'intensità
            pulse = math.sin(self.animation_step * 0.3) * 0.2 + 1.0
            radius = 60 * pulse * self.intensity
            
            # Cerchio esterno (tono)
            self.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                fill=color, outline=color, width=2
            )
            
            # Cerchio interno (confidenza)
            inner_radius = radius * self.confidence
            self.create_oval(
                center_x - inner_radius, center_y - inner_radius,
                center_x + inner_radius, center_y + inner_radius,
                fill="white", outline="white"
            )
            
            # Onde concentriche
            for i in range(3):
                wave_radius = 80 + i * 20
                alpha = 0.3 * math.sin(self.animation_step * 0.2 - i * 0.5)
                if alpha > 0:
                    wave_color = color
                    self.create_oval(
                        center_x - wave_radius, center_y - wave_radius,
                        center_x + wave_radius, center_y + wave_radius,
                        outline=wave_color, width=2
                    )
            
            # Testo del tono
            self.create_text(
                center_x, center_y + radius + 30,
                text=f"Tono: {self.current_tone.title()}",
                fill="white", font=("Arial", 12, "bold")
            )
            
            self.create_text(
                center_x, center_y + radius + 50,
                text=f"Intensità: {self.intensity:.1f} | Confidenza: {self.confidence:.0%}",
                fill="lightgray", font=("Arial", 10)
            )
        else:
            # Stato di riposo
            self.create_oval(
                center_x - 50, center_y - 50,
                center_x + 50, center_y + 50,
                fill="#404040", outline="#606060", width=2
            )
            
            self.create_text(
                center_x, center_y,
                text="Premi per\nregistrare",
                fill="lightgray", font=("Arial", 12), justify=tk.CENTER
            )
        
        self.animation_step += 1
        self.after(100, self.animate)  # Aggiorna ogni 100ms

class MainWindowTk:
    """Finestra principale con Tkinter"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎤 VibeTalking - Audio Recorder & Tone Analyzer (Demo)")
        self.root.geometry("800x700")
        self.root.configure(bg='#2b2b2b')
        
        # Componenti
        self.audio_recorder = AudioRecorder()
        self.ai_analyzer = AudioAnalyzer()
        self.current_recording_path = None
        self.is_recording = False
        
        self.create_ui()
        
        # Verifica configurazione
        try:
            Config.validate_config()
            self.update_status("✅ Modalità demo attiva - Pronto per registrare")
        except Exception as e:
            self.update_status(f"❌ Errore configurazione: {e}")
            self.record_button.configure(state='disabled')
    
    def create_ui(self):
        """Crea l'interfaccia utente"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="🎤 VibeTalking Demo",
            font=("Arial", 24, "bold"),
            bg='#2b2b2b', fg='white'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Registrazione Audio con Analisi del Tono AI - Modalità Demo",
            font=("Arial", 12),
            bg='#2b2b2b', fg='lightgray'
        )
        subtitle_label.pack()
        
        # Info demo
        demo_info = tk.Label(
            header_frame,
            text="⚠️ Versione demo offline - simula registrazione e analisi AI",
            font=("Arial", 10, "italic"),
            bg='#2b2b2b', fg='orange'
        )
        demo_info.pack(pady=5)
        
        # Visualizzatore del tono
        viz_frame = ttk.Frame(main_frame)
        viz_frame.pack(pady=20)
        
        self.tone_visualizer = ToneVisualizerTk(viz_frame)
        self.tone_visualizer.pack()
        
        # Controlli
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(pady=20)
        
        self.record_button = tk.Button(
            controls_frame,
            text="🎤 Inizia Registrazione",
            font=("Arial", 12, "bold"),
            width=20, height=2,
            command=self.on_record_clicked,
            bg='#4CAF50', fg='white',
            activebackground='#45a049'
        )
        self.record_button.pack(side=tk.LEFT, padx=10)
        
        self.analyze_button = tk.Button(
            controls_frame,
            text="🔍 Analizza Ultimo",
            font=("Arial", 12),
            width=20, height=2,
            command=self.on_analyze_clicked,
            bg='#2196F3', fg='white',
            activebackground='#1976D2',
            state='disabled'
        )
        self.analyze_button.pack(side=tk.LEFT, padx=10)
        
        settings_button = tk.Button(
            controls_frame,
            text="⚙️ Info",
            font=("Arial", 12),
            width=15, height=2,
            command=self.on_settings_clicked,
            bg='#FF9800', fg='white',
            activebackground='#F57C00'
        )
        settings_button.pack(side=tk.LEFT, padx=10)
        
        # Area risultati
        results_frame = ttk.LabelFrame(main_frame, text="Risultati Analisi", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=10,
            font=("Consolas", 10),
            bg='#1e1e1e', fg='white',
            insertbackground='white'
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Pronto")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 10, "italic"),
            bg='#2b2b2b', fg='lightgray'
        )
        status_label.pack(pady=(10, 0))
    
    def on_record_clicked(self):
        """Gestisce il click del pulsante registrazione"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Inizia la registrazione"""
        if self.audio_recorder.start_recording():
            self.is_recording = True
            self.record_button.configure(
                text="⏹️ Ferma Registrazione",
                bg='#f44336'
            )
            self.tone_visualizer.set_recording_state(True)
            self.update_status("🎤 Registrazione in corso (simulazione)...")
            self.analyze_button.configure(state='disabled')
        else:
            self.update_status("❌ Errore nell'avvio della registrazione")
    
    def stop_recording(self):
        """Ferma la registrazione"""
        self.current_recording_path = self.audio_recorder.stop_recording()
        self.is_recording = False
        self.record_button.configure(
            text="🎤 Inizia Registrazione",
            bg='#4CAF50'
        )
        self.tone_visualizer.set_recording_state(False)
        
        if self.current_recording_path:
            self.update_status(f"✅ Registrazione salvata: {Path(self.current_recording_path).name}")
            self.analyze_button.configure(state='normal')
        else:
            self.update_status("❌ Errore nel salvataggio della registrazione")
    
    def on_analyze_clicked(self):
        """Gestisce il click del pulsante analisi"""
        if not self.current_recording_path:
            self.update_status("❌ Nessuna registrazione da analizzare")
            return
        
        self.analyze_button.configure(state='disabled')
        self.record_button.configure(state='disabled')
        self.update_status("🔄 Analisi in corso (simulazione)...")
        self.clear_results()
        
        # Avvia l'analisi in un thread separato
        thread = threading.Thread(target=self.run_analysis)
        thread.daemon = True
        thread.start()
    
    def run_analysis(self):
        """Esegue l'analisi AI in background"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            results = loop.run_until_complete(
                self.ai_analyzer.full_analysis(self.current_recording_path)
            )
            
            # Aggiorna l'UI nel thread principale
            self.root.after(0, lambda: self.on_analysis_complete(results))
            
        except Exception as e:
            error_msg = f"Errore nell'analisi: {e}"
            self.root.after(0, lambda: self.on_analysis_error(error_msg))
        finally:
            loop.close()
    
    def on_analysis_complete(self, results):
        """Chiamata quando l'analisi è completata"""
        self.analyze_button.configure(state='normal')
        self.record_button.configure(state='normal')
        
        # Aggiorna la visualizzazione del tono
        if results.get("tone_analysis"):
            self.tone_visualizer.update_tone(results["tone_analysis"])
        
        # Mostra i risultati
        self.display_results(results)
        
        # Salva i risultati
        if Config.SAVE_TONE_ANALYSIS:
            output_file = self.ai_analyzer.save_analysis_results(results)
            self.update_status(f"✅ Analisi completata - Risultati salvati in {Path(output_file).name}")
        else:
            self.update_status("✅ Analisi completata")
    
    def on_analysis_error(self, error_msg):
        """Chiamata in caso di errore nell'analisi"""
        self.analyze_button.configure(state='normal')
        self.record_button.configure(state='normal')
        self.update_status(f"❌ {error_msg}")
    
    def display_results(self, results):
        """Mostra i risultati nell'area di testo"""
        self.results_text.delete(1.0, tk.END)
        
        # Trascrizione
        if results.get("transcription"):
            self.results_text.insert(tk.END, "📝 TRASCRIZIONE:\n")
            self.results_text.insert(tk.END, f"{results['transcription']}\n\n")
        
        # Riassunto
        if results.get("summary"):
            self.results_text.insert(tk.END, "📋 RIASSUNTO:\n")
            self.results_text.insert(tk.END, f"{results['summary']}\n\n")
        
        # Analisi del tono
        if results.get("tone_analysis"):
            tone = results["tone_analysis"]
            self.results_text.insert(tk.END, "🎭 ANALISI DEL TONO:\n")
            self.results_text.insert(tk.END, f"Tono principale: {tone.get('tono_principale', 'N/A')}\n")
            self.results_text.insert(tk.END, f"Intensità: {tone.get('intensità', 'N/A')}\n")
            self.results_text.insert(tk.END, f"Confidenza: {tone.get('confidenza', 'N/A')}%\n")
            
            if tone.get("emozioni_secondarie"):
                self.results_text.insert(tk.END, f"Emozioni secondarie: {', '.join(tone['emozioni_secondarie'])}\n")
            
            if tone.get("descrizione"):
                self.results_text.insert(tk.END, f"Descrizione: {tone['descrizione']}\n")
            
            if tone.get("suggerimenti"):
                self.results_text.insert(tk.END, "💡 Suggerimenti:\n")
                for suggestion in tone["suggerimenti"]:
                    self.results_text.insert(tk.END, f"  • {suggestion}\n")
        
        # Scroll alla fine
        self.results_text.see(tk.END)
    
    def clear_results(self):
        """Pulisce l'area dei risultati"""
        self.results_text.delete(1.0, tk.END)
    
    def on_settings_clicked(self):
        """Apre la finestra delle informazioni"""
        info_text = (
            "🎤 VibeTalking Demo\n\n"
            "Questa è una versione demo che simula:\n"
            "• Registrazione audio (genera file WAV fittizi)\n"
            "• Trascrizione automatica (testi di esempio)\n"
            "• Analisi del tono (basata su parole chiave)\n"
            "• Visualizzazione dinamica del tono\n\n"
            f"Directory output: {Config.OUTPUT_DIR}\n"
            f"Sample rate: {Config.SAMPLE_RATE} Hz\n"
            f"Canali: {Config.CHANNELS}\n\n"
            "Per la versione completa con AI reale,\n"
            "configura GOOGLE_API_KEY nel file .env"
        )
        messagebox.showinfo("Informazioni Demo", info_text)
    
    def update_status(self, message):
        """Aggiorna la status bar"""
        self.status_var.set(message)
        print(message)  # Log anche in console
    
    def run(self):
        """Avvia l'applicazione"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
    
    def on_closing(self):
        """Cleanup quando la finestra viene chiusa"""
        if self.is_recording:
            self.audio_recorder.stop_recording()
        
        self.audio_recorder.cleanup()
        self.root.destroy()

def main():
    """Funzione principale dell'applicazione"""
    print("🎤 Avvio VibeTalking Demo...")
    
    try:
        # Verifica la configurazione
        Config.validate_config()
        print("✅ Configurazione validata")
        
        # Crea e avvia l'applicazione
        app = MainWindowTk()
        print("🚀 Applicazione demo avviata con successo!")
        print(f"📁 Directory output: {Config.OUTPUT_DIR}")
        
        app.run()
        
    except Exception as e:
        print(f"❌ Errore nell'avvio dell'applicazione: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
