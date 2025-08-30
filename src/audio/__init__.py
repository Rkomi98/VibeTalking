# Usa sempre la versione demo per evitare crash Linux con PyAudio/XCB
import importlib.util
import shutil

# Ordine di preferenza backend: arecord → pyaudio → demo

def _has_arecord() -> bool:
    return shutil.which("arecord") is not None

def _has_pyaudio() -> bool:
    return importlib.util.find_spec("pyaudio") is not None

try:
    if _has_arecord():
        from .recorder_arecord import AudioRecorder  # type: ignore
        print("🔧 Usando AudioRecorder reale (arecord/ALSA)")
    elif _has_pyaudio():
        from .recorder_pyaudio import AudioRecorder  # type: ignore
        print("🔧 Usando AudioRecorder reale (PyAudio)")
    else:
        from .recorder_demo import AudioRecorder  # type: ignore
        print("🔧 Usando AudioRecorder demo (stabile su Linux)")
except Exception as e:
    from .recorder_demo import AudioRecorder  # type: ignore
    print(f"⚠️ Errore backend audio ({e}), uso demo")

__all__ = ['AudioRecorder']