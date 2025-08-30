"""
Registratore audio reale basato su arecord (ALSA)

Richiede che 'arecord' sia disponibile nel sistema.
"""
from __future__ import annotations

import subprocess
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

from ..config import Config


class AudioRecorder:
    """Registra audio dal microfono usando 'arecord' (ALSA)."""

    def __init__(self) -> None:
        self.process: Optional[subprocess.Popen] = None
        self.is_recording: bool = False
        self.current_filepath: Optional[str] = None
        self.callback: Optional[Callable[[bytes], None]] = None
        self._reader_thread: Optional[threading.Thread] = None

    def set_callback(self, callback: Callable[[bytes], None]) -> None:
        self.callback = callback

    def _reader_loop(self) -> None:
        assert self.process is not None
        try:
            while self.is_recording:
                chunk = self.process.stdout.read(Config.CHUNK_SIZE * 2)
                if not chunk:
                    break
                if self.callback:
                    self.callback(chunk)
        except Exception:
            pass

    def start_recording(self) -> str:
        if self.is_recording:
            return ""

        # Assicura la cartella output
        Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.{Config.AUDIO_FORMAT}"
        filepath = Config.OUTPUT_DIR / filename
        self.current_filepath = str(filepath)

        # Comando arecord (16-bit little-endian, mono, sample rate da config)
        # -f S16_LE: formato 16-bit PCM
        # -c 1: mono (usa Config.CHANNELS se serve)
        # -r <rate>: sample rate
        # -t wav: output WAV
        # -q: quiet
        cmd = [
            "arecord",
            "-q",
            "-f",
            "S16_LE",
            "-c",
            str(Config.CHANNELS),
            "-r",
            str(Config.SAMPLE_RATE),
            "-t",
            "wav",
            self.current_filepath,
        ]

        try:
            # Avvio processo arecord
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0,
            )
            self.is_recording = True

            # Thread che legge stdout per callback (quando si usa -t wav, i dati non sempre arrivano su stdout)
            if self.process.stdout and self.callback:
                self._reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
                self._reader_thread.start()

            print("🎤 Registrazione iniziata (arecord)...")
            return self.current_filepath

        except FileNotFoundError:
            print("❌ 'arecord' non trovato. Installa alsa-utils.")
            self.is_recording = False
            return ""
        except Exception as e:
            print(f"❌ Errore avvio arecord: {e}")
            self.is_recording = False
            return ""

    def stop_recording(self) -> Optional[str]:
        if not self.is_recording or not self.current_filepath:
            return None

        try:
            self.is_recording = False
            if self.process and self.process.poll() is None:
                self.process.terminate()
                try:
                    self.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.process.kill()

            if self._reader_thread and self._reader_thread.is_alive():
                self._reader_thread.join(timeout=1.0)

            print(f"💾 Registrazione salvata: {self.current_filepath}")
            return self.current_filepath
        except Exception as e:
            print(f"❌ Errore stop arecord: {e}")
            return None
        finally:
            self.process = None
            self._reader_thread = None

    def cleanup(self) -> None:
        if self.is_recording:
            self.stop_recording()

    def __del__(self) -> None:
        self.cleanup()


