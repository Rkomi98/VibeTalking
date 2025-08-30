from .analyzer import AudioAnalyzer

# Prova a importare DataPizzaAudioAnalyzer
try:
    from .datapizza_analyzer import DataPizzaAudioAnalyzer
    print("🔧 DataPizzaAudioAnalyzer disponibile")
    __all__ = ['AudioAnalyzer', 'DataPizzaAudioAnalyzer']
except ImportError as e:
    print(f"⚠️ DataPizzaAudioAnalyzer non disponibile: {e}")
    __all__ = ['AudioAnalyzer']
