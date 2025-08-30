"""
Finestra principale dell'applicazione VibeTalking
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Pango
import asyncio
import threading
from pathlib import Path
from typing import Optional

from .tone_visualizer import ToneVisualizer
from ..audio import AudioRecorder
from ..ai import AudioAnalyzer
from ..config import Config

class MainWindow(Gtk.Window):
    """Finestra principale dell'applicazione"""
    
    def __init__(self):
        super().__init__(title=Config.WINDOW_TITLE)
        
        # Configura finestra
        self.set_default_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", self.on_destroy)
        
        # Componenti
        self.audio_recorder = AudioRecorder()
        self.ai_analyzer = AudioAnalyzer()
        self.current_recording_path = None
        self.is_recording = False
        
        # Crea interfaccia
        self.create_ui()
        
        # Verifica configurazione
        try:
            Config.validate_config()
            self.update_status("✅ Configurazione valida - Pronto per registrare")
        except ValueError as e:
            self.update_status(f"❌ Errore configurazione: {e}")
            self.record_button.set_sensitive(False)
    
    def create_ui(self):
        """Crea l'interfaccia utente"""
        # Layout principale
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_left(20)
        main_box.set_margin_right(20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        self.add(main_box)
        
        # Header
        header_box = self.create_header()
        main_box.pack_start(header_box, False, False, 0)
        
        # Visualizzatore del tono
        self.tone_visualizer = ToneVisualizer()
        main_box.pack_start(self.tone_visualizer, True, True, 0)
        
        # Controlli
        controls_box = self.create_controls()
        main_box.pack_start(controls_box, False, False, 0)
        
        # Area risultati
        results_box = self.create_results_area()
        main_box.pack_start(results_box, True, True, 0)
        
        # Status bar
        self.status_label = Gtk.Label()
        self.status_label.set_markup("<i>Pronto</i>")
        main_box.pack_start(self.status_label, False, False, 0)
    
    def create_header(self):
        """Crea l'header dell'applicazione"""
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        # Titolo
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>🎤 VibeTalking</span>")
        header_box.pack_start(title_label, False, False, 0)
        
        # Sottotitolo
        subtitle_label = Gtk.Label()
        subtitle_label.set_markup("<span size='small'>Registrazione Audio con Analisi del Tono AI</span>")
        subtitle_label.set_sensitive(False)
        header_box.pack_start(subtitle_label, False, False, 0)
        
        return header_box
    
    def create_controls(self):
        """Crea i controlli principali"""
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        controls_box.set_halign(Gtk.Align.CENTER)
        
        # Pulsante registrazione
        self.record_button = Gtk.Button()
        self.record_button.set_size_request(150, 50)
        self.update_record_button()
        self.record_button.connect("clicked", self.on_record_clicked)
        controls_box.pack_start(self.record_button, False, False, 0)
        
        # Pulsante analisi
        self.analyze_button = Gtk.Button(label="🔍 Analizza Ultimo")
        self.analyze_button.set_size_request(150, 50)
        self.analyze_button.set_sensitive(False)
        self.analyze_button.connect("clicked", self.on_analyze_clicked)
        controls_box.pack_start(self.analyze_button, False, False, 0)
        
        # Pulsante impostazioni
        settings_button = Gtk.Button(label="⚙️ Impostazioni")
        settings_button.set_size_request(120, 50)
        settings_button.connect("clicked", self.on_settings_clicked)
        controls_box.pack_start(settings_button, False, False, 0)
        
        return controls_box
    
    def create_results_area(self):
        """Crea l'area per mostrare i risultati"""
        frame = Gtk.Frame(label="Risultati Analisi")
        frame.set_size_request(-1, 200)
        
        # Scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        frame.add(scrolled)
        
        # Text view per i risultati
        self.results_textview = Gtk.TextView()
        self.results_textview.set_editable(False)
        self.results_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        
        # Font monospace per i risultati
        font_desc = Pango.FontDescription("monospace 10")
        self.results_textview.modify_font(font_desc)
        
        scrolled.add(self.results_textview)
        
        return frame
    
    def update_record_button(self):
        """Aggiorna il pulsante di registrazione"""
        if self.is_recording:
            self.record_button.set_label("⏹️ Ferma Registrazione")
            self.record_button.get_style_context().add_class("destructive-action")
        else:
            self.record_button.set_label("🎤 Inizia Registrazione")
            self.record_button.get_style_context().remove_class("destructive-action")
    
    def on_record_clicked(self, button):
        """Gestisce il click del pulsante registrazione"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Inizia la registrazione"""
        if self.audio_recorder.start_recording():
            self.is_recording = True
            self.update_record_button()
            self.tone_visualizer.set_recording_state(True)
            self.update_status("🎤 Registrazione in corso...")
            
            # Disabilita il pulsante analisi
            self.analyze_button.set_sensitive(False)
        else:
            self.update_status("❌ Errore nell'avvio della registrazione")
    
    def stop_recording(self):
        """Ferma la registrazione"""
        self.current_recording_path = self.audio_recorder.stop_recording()
        self.is_recording = False
        self.update_record_button()
        self.tone_visualizer.set_recording_state(False)
        
        if self.current_recording_path:
            self.update_status(f"✅ Registrazione salvata: {Path(self.current_recording_path).name}")
            self.analyze_button.set_sensitive(True)
        else:
            self.update_status("❌ Errore nel salvataggio della registrazione")
    
    def on_analyze_clicked(self, button):
        """Gestisce il click del pulsante analisi"""
        if not self.current_recording_path:
            self.update_status("❌ Nessuna registrazione da analizzare")
            return
        
        # Disabilita i pulsanti durante l'analisi
        self.analyze_button.set_sensitive(False)
        self.record_button.set_sensitive(False)
        
        self.update_status("🔄 Analisi in corso...")
        self.clear_results()
        
        # Avvia l'analisi in un thread separato
        thread = threading.Thread(target=self.run_analysis)
        thread.daemon = True
        thread.start()
    
    def run_analysis(self):
        """Esegue l'analisi AI in background"""
        try:
            # Crea un nuovo event loop per questo thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Esegue l'analisi
            results = loop.run_until_complete(
                self.ai_analyzer.full_analysis(self.current_recording_path)
            )
            
            # Aggiorna l'UI nel thread principale
            GLib.idle_add(self.on_analysis_complete, results)
            
        except Exception as e:
            error_msg = f"Errore nell'analisi: {e}"
            GLib.idle_add(self.on_analysis_error, error_msg)
        finally:
            loop.close()
    
    def on_analysis_complete(self, results):
        """Chiamata quando l'analisi è completata"""
        # Riabilita i pulsanti
        self.analyze_button.set_sensitive(True)
        self.record_button.set_sensitive(True)
        
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
        self.analyze_button.set_sensitive(True)
        self.record_button.set_sensitive(True)
        self.update_status(f"❌ {error_msg}")
    
    def display_results(self, results):
        """Mostra i risultati nell'area di testo"""
        buffer = self.results_textview.get_buffer()
        
        # Trascrizione
        if results.get("transcription"):
            buffer.insert_at_cursor("📝 TRASCRIZIONE:\n")
            buffer.insert_at_cursor(f"{results['transcription']}\n\n")
        
        # Riassunto
        if results.get("summary"):
            buffer.insert_at_cursor("📋 RIASSUNTO:\n")
            buffer.insert_at_cursor(f"{results['summary']}\n\n")
        
        # Analisi del tono
        if results.get("tone_analysis"):
            tone = results["tone_analysis"]
            buffer.insert_at_cursor("🎭 ANALISI DEL TONO:\n")
            buffer.insert_at_cursor(f"Tono principale: {tone.get('tono_principale', 'N/A')}\n")
            buffer.insert_at_cursor(f"Intensità: {tone.get('intensità', 'N/A')}\n")
            buffer.insert_at_cursor(f"Confidenza: {tone.get('confidenza', 'N/A')}%\n")
            
            if tone.get("emozioni_secondarie"):
                buffer.insert_at_cursor(f"Emozioni secondarie: {', '.join(tone['emozioni_secondarie'])}\n")
            
            if tone.get("descrizione"):
                buffer.insert_at_cursor(f"Descrizione: {tone['descrizione']}\n")
            
            if tone.get("suggerimenti"):
                buffer.insert_at_cursor("💡 Suggerimenti:\n")
                for suggestion in tone["suggerimenti"]:
                    buffer.insert_at_cursor(f"  • {suggestion}\n")
        
        # Scroll alla fine
        mark = buffer.get_insert()
        self.results_textview.scroll_mark_onscreen(mark)
    
    def clear_results(self):
        """Pulisce l'area dei risultati"""
        buffer = self.results_textview.get_buffer()
        buffer.set_text("")
    
    def on_settings_clicked(self, button):
        """Apre la finestra delle impostazioni"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Impostazioni"
        )
        dialog.format_secondary_text(
            f"Directory output: {Config.OUTPUT_DIR}\n"
            f"Sample rate: {Config.SAMPLE_RATE} Hz\n"
            f"Canali: {Config.CHANNELS}\n"
            f"Analisi tono: {'Abilitata' if Config.TONE_ANALYSIS_ENABLED else 'Disabilitata'}"
        )
        dialog.run()
        dialog.destroy()
    
    def update_status(self, message):
        """Aggiorna la status bar"""
        self.status_label.set_markup(f"<i>{message}</i>")
        print(message)  # Log anche in console
    
    def on_destroy(self, widget):
        """Cleanup quando la finestra viene chiusa"""
        if self.is_recording:
            self.audio_recorder.stop_recording()
        
        self.audio_recorder.cleanup()
        Gtk.main_quit()
