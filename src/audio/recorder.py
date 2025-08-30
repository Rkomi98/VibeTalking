"""
Modulo per la registrazione audio
"""
import pyaudio
import wave
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable

from ..config import Config

class AudioRecorder:
    """Classe per gestire la registrazione audio"""
    
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.is_recording = False
        self.frames = []
        self.stream = None
        self.recording_thread = None
        self.callback = None
        
    def set_callback(self, callback: Callable[[bytes], None]):
        """Imposta una callback per ricevere i dati audio in tempo reale"""
        self.callback = callback
        
    def start_recording(self) -> bool:
        """Inizia la registrazione audio"""
        if self.is_recording:
            return False
            
        try:
            self.frames = []
            self.is_recording = True
            
            # Configura lo stream audio
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=Config.CHANNELS,
                rate=Config.SAMPLE_RATE,
                input=True,
                frames_per_buffer=Config.CHUNK_SIZE,
                stream_callback=self._audio_callback
            )
            
            self.stream.start_stream()
            print("🎤 Registrazione iniziata...")
            return True
            
        except Exception as e:
            print(f"❌ Errore nell'avvio della registrazione: {e}")
            self.is_recording = False
            return False
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback per processare i dati audio in tempo reale"""
        if self.is_recording:
            self.frames.append(in_data)
            
            # Chiama la callback esterna se impostata
            if self.callback:
                self.callback(in_data)
                
        return (in_data, pyaudio.paContinue)
    
    def stop_recording(self) -> Optional[str]:
        """Ferma la registrazione e salva il file"""
        if not self.is_recording:
            return None
            
        self.is_recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        # Genera nome file con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.{Config.AUDIO_FORMAT}"
        filepath = Config.OUTPUT_DIR / filename
        
        # Salva il file audio
        try:
            with wave.open(str(filepath), 'wb') as wf:
                wf.setnchannels(Config.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(Config.SAMPLE_RATE)
                wf.writeframes(b''.join(self.frames))
            
            print(f"💾 Registrazione salvata: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Errore nel salvataggio: {e}")
            return None
    
    def get_recording_duration(self) -> float:
        """Restituisce la durata della registrazione corrente in secondi"""
        if not self.frames:
            return 0.0
        
        total_frames = len(self.frames) * Config.CHUNK_SIZE
        return total_frames / Config.SAMPLE_RATE
    
    def cleanup(self):
        """Pulisce le risorse audio"""
        if self.is_recording:
            self.stop_recording()
        
        if self.audio:
            self.audio.terminate()
    
    def __del__(self):
        """Distruttore per pulire le risorse"""
        self.cleanup()
