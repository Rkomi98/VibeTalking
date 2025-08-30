"""
Registratore audio demo - simulazione senza PyAudio per evitare crash Linux
"""
import time
import math
import struct
import wave
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable
import threading

from ..config import Config


class AudioRecorder:
    """Registratore audio demo che simula la registrazione"""
    
    def __init__(self):
        self.is_recording = False
        self.frames: list[bytes] = []
        self.callback: Optional[Callable[[bytes], None]] = None
        self.recording_thread: Optional[threading.Thread] = None
        self.start_time = 0.0
        self.current_filepath: Optional[str] = None
        
    def set_callback(self, callback: Callable[[bytes], None]) -> None:
        """Imposta callback per i dati audio"""
        self.callback = callback
    
    def start_recording(self) -> str:
        """Avvia la registrazione simulata"""
        if self.is_recording:
            return ""
            
        # Crea il percorso del file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.{Config.AUDIO_FORMAT}"
        filepath = Config.OUTPUT_DIR / filename
        self.current_filepath = str(filepath)
        
        # Avvia la simulazione
        self.frames = []
        self.is_recording = True
        self.start_time = time.time()
        
        self.recording_thread = threading.Thread(target=self._simulate_recording)
        self.recording_thread.daemon = True
        self.recording_thread.start()
        
        print("🎤 Registrazione iniziata (simulazione)...")
        return self.current_filepath
    
    def stop_recording(self) -> Optional[str]:
        """Ferma la registrazione e salva il file"""
        if not self.is_recording or not self.current_filepath:
            return None
            
        self.is_recording = False
        
        # Aspetta che il thread finisca
        if self.recording_thread:
            self.recording_thread.join(timeout=2.0)
        
        # Salva il file WAV
        try:
            with wave.open(self.current_filepath, 'wb') as wf:
                wf.setnchannels(Config.CHANNELS)
                wf.setsampwidth(2)  # 16 bit = 2 bytes
                wf.setframerate(Config.SAMPLE_RATE)
                wf.writeframes(b''.join(self.frames))
            
            print(f"💾 Registrazione salvata: {self.current_filepath}")
            return self.current_filepath
            
        except Exception as e:
            print(f"❌ Errore salvataggio: {e}")
            return None
    
    def _simulate_recording(self):
        """Simula la registrazione generando audio sintetico"""
        chunk_duration = Config.CHUNK_SIZE / Config.SAMPLE_RATE
        
        while self.is_recording:
            # Genera un chunk di audio
            audio_data = []
            current_time = time.time() - self.start_time
            
            for i in range(Config.CHUNK_SIZE):
                t = current_time + (i / Config.SAMPLE_RATE)
                
                # Genera un segnale complesso più realistico
                # Tono base a 440Hz (La)
                base_tone = math.sin(2 * math.pi * 440 * t)
                
                # Aggiunge armoniche per rendere più realistico
                harmonic1 = 0.3 * math.sin(2 * math.pi * 880 * t)  # Ottava
                harmonic2 = 0.2 * math.sin(2 * math.pi * 1320 * t)  # Quinta
                
                # Modulazione di ampiezza per variazione
                amplitude_mod = 0.8 + 0.2 * math.sin(2 * math.pi * 0.5 * t)
                
                # Rumore per realismo
                import random
                noise = 0.1 * (random.random() - 0.5)
                
                # Combina tutti i segnali
                sample = amplitude_mod * (base_tone + harmonic1 + harmonic2) + noise
                
                # Scala e converte a 16-bit
                sample_16bit = int(sample * 15000)  # Ampiezza ragionevole
                sample_16bit = max(-32768, min(32767, sample_16bit))  # Clamp
                
                audio_data.append(sample_16bit)
            
            # Converte in bytes
            audio_bytes = struct.pack('<' + 'h' * len(audio_data), *audio_data)
            self.frames.append(audio_bytes)
            
            # Chiama il callback se presente
            if self.callback:
                self.callback(audio_bytes)
            
            # Aspetta per simulare il tempo reale
            time.sleep(chunk_duration)
    
    def cleanup(self):
        """Pulisce le risorse"""
        if self.is_recording:
            self.stop_recording()
    
    def __del__(self):
        self.cleanup()
