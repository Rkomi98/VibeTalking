"""
Modulo per la registrazione audio (versione demo)
"""
import threading
import time
import wave
import struct
import math
import random
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable

from ..config import Config

class AudioRecorder:
    """Classe per gestire la registrazione audio"""
    
    def __init__(self):
        # Modalità demo - simula la registrazione audio
        self.is_recording = False
        self.frames = []
        self.recording_thread = None
        self.callback = None
        self.start_time = None
        self.phase = 0.0
        print("🔧 Modalità demo audio - simulazione registrazione")
        
    def set_callback(self, callback: Callable[[bytes], None]):
        """Imposta una callback per ricevere i dati audio in tempo reale"""
        self.callback = callback
        
    def start_recording(self) -> bool:
        """Inizia la registrazione audio (simulata)"""
        if self.is_recording:
            return False
            
        try:
            self.frames = []
            self.is_recording = True
            self.start_time = time.time()
            
            # Avvia il thread di simulazione
            self.recording_thread = threading.Thread(target=self._simulate_recording)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            print("🎤 Registrazione iniziata (simulazione)...")
            return True
            
        except Exception as e:
            print(f"❌ Errore nell'avvio della registrazione: {e}")
            self.is_recording = False
            return False
    
    def _simulate_recording(self):
        """Simula la registrazione audio generando dati fittizi"""
        frequency_hz = 440.0
        sample_rate = Config.SAMPLE_RATE
        channels = Config.CHANNELS
        phase_increment = 2 * math.pi * frequency_hz / sample_rate
        amplitude_signal = 10000  # Ampiezza principale udibile
        amplitude_noise = 1500    # Rumore di fondo
        while self.is_recording:
            # Genera dati audio fittizi (silenzio con un po' di rumore)
            chunk_size = Config.CHUNK_SIZE
            
            # Genera un chunk di dati audio simulati
            audio_data = []
            for _ in range(chunk_size):
                # Segnale sinusoidale continuo
                s = int(amplitude_signal * math.sin(self.phase))
                self.phase += phase_increment
                if self.phase > 2 * math.pi:
                    self.phase -= 2 * math.pi
                # Aggiungi rumore bianco leggero
                s += int(random.uniform(-amplitude_noise, amplitude_noise))
                # Clamping a 16-bit
                if s > 32767:
                    s = 32767
                elif s < -32768:
                    s = -32768
                if channels == 2:
                    # Duplica per stereo
                    audio_data.extend([s, s])
                else:
                    audio_data.append(s)
            
            # Converte in bytes
            audio_bytes = struct.pack('<' + ('h' * len(audio_data)), *audio_data)
            self.frames.append(audio_bytes)
            
            # Chiama la callback se impostata
            if self.callback:
                self.callback(audio_bytes)
            
            # Aspetta per simulare il tempo reale
            # Se stereo, abbiamo generato 2 campioni per frame
            effective_chunk = chunk_size
            time.sleep(effective_chunk / sample_rate)
    
    def stop_recording(self) -> Optional[str]:
        """Ferma la registrazione e salva il file"""
        if not self.is_recording:
            return None
            
        self.is_recording = False
        
        # Aspetta che il thread di simulazione finisca
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=1)
        
        # Genera nome file con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.{Config.AUDIO_FORMAT}"
        filepath = Config.OUTPUT_DIR / filename
        
        # Salva il file audio simulato
        try:
            with wave.open(str(filepath), 'wb') as wf:
                wf.setnchannels(Config.CHANNELS)
                wf.setsampwidth(2)  # 16-bit = 2 bytes
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
        
        # In modalità demo non ci sono risorse da pulire
    
    def __del__(self):
        """Distruttore per pulire le risorse"""
        self.cleanup()
