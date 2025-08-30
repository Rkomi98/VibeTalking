"""
Registratore audio reale basato su PyAudio
"""
from typing import Optional, Callable, TYPE_CHECKING
from datetime import datetime
from pathlib import Path
import wave

from ..config import Config

if TYPE_CHECKING:
    import pyaudio

class AudioRecorder:
    """Registra audio dal microfono usando PyAudio"""

    def __init__(self) -> None:
        self.audio: Optional["pyaudio.PyAudio"] = None
        self.stream = None
        self.frames: list[bytes] = []
        self.is_recording = False
        self.callback: Optional[Callable[[bytes], None]] = None
        self.current_filepath: Optional[str] = None

    def set_callback(self, callback: Callable[[bytes], None]) -> None:
        self.callback = callback

    def _stream_callback(self, in_data, frame_count, time_info, status):
        import pyaudio
        if self.is_recording and in_data:
            self.frames.append(in_data)
            if self.callback:
                self.callback(in_data)
        return (in_data, pyaudio.paContinue)

    def start_recording(self) -> str:
        import pyaudio
        if self.is_recording:
            return ""
        try:
            if not self.audio:
                self.audio = pyaudio.PyAudio()

            self.frames = []
            self.is_recording = True
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=Config.CHANNELS,
                rate=Config.SAMPLE_RATE,
                input=True,
                frames_per_buffer=Config.CHUNK_SIZE,
                stream_callback=self._stream_callback,
            )
            self.stream.start_stream()
            print("🎤 Registrazione iniziata (microfono)...")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.{Config.AUDIO_FORMAT}"
            filepath = Config.OUTPUT_DIR / filename
            self.current_filepath = str(filepath)
            return self.current_filepath

        except Exception as e:
            print(f"❌ Errore apertura stream microfono: {e}")
            self.is_recording = False
            if self.stream:
                try:
                    self.stream.close()
                except Exception:
                    pass
            if self.audio:
                self.audio.terminate()
                self.audio = None
            return ""

    def stop_recording(self) -> Optional[str]:
        import pyaudio
        if not self.is_recording or not self.current_filepath:
            return None
        self.is_recording = False
        try:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
        finally:
            self.stream = None

        filepath = self.current_filepath

        try:
            with wave.open(str(filepath), "wb") as wf:
                wf.setnchannels(Config.CHANNELS)
                if self.audio:
                    wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                else:
                    wf.setsampwidth(2) 
                wf.setframerate(Config.SAMPLE_RATE)
                wf.writeframes(b"".join(self.frames))
            print(f"💾 Registrazione salvata: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Errore salvaggio WAV: {e}")
            return None

    def cleanup(self) -> None:
        if self.is_recording:
            self.stop_recording()
        try:
            if self.audio:
                self.audio.terminate()
                self.audio = None
        except Exception:
            pass

    def __del__(self) -> None:
        self.cleanup()


