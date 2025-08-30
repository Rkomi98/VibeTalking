"""
Configurazione dell'applicazione VibeTalking
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Carica le variabili d'ambiente
load_dotenv()

class Config:
    """Classe per la gestione della configurazione"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Configurazione Audio
    SAMPLE_RATE = int(os.getenv('DEFAULT_SAMPLE_RATE', 44100))
    CHANNELS = int(os.getenv('DEFAULT_CHANNELS', 1))
    AUDIO_FORMAT = os.getenv('AUDIO_FORMAT', 'wav')
    CHUNK_SIZE = 1024
    
    # Configurazione Analisi
    TONE_ANALYSIS_ENABLED = os.getenv('TONE_ANALYSIS_ENABLED', 'true').lower() == 'true'
    ANIMATION_ENABLED = os.getenv('ANIMATION_ENABLED', 'true').lower() == 'true'
    
    # Configurazione Output
    OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', './recordings'))
    SAVE_TRANSCRIPTION = os.getenv('SAVE_TRANSCRIPTION', 'true').lower() == 'true'
    SAVE_TONE_ANALYSIS = os.getenv('SAVE_TONE_ANALYSIS', 'true').lower() == 'true'
    
    # Configurazione GUI
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    WINDOW_TITLE = "VibeTalking - Audio Recorder & Tone Analyzer"
    
    @classmethod
    def validate_config(cls):
        """Valida la configurazione"""
        # In modalità demo, l'API key non è richiesta
        if not cls.GOOGLE_API_KEY:
            print("⚠️ GOOGLE_API_KEY non trovata - modalità demo attiva")
        
        # Crea la directory di output se non esiste
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        return True
