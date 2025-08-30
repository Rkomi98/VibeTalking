#!/usr/bin/env python3
"""
Script di test per verificare le funzionalità di VibeTalking
"""
import sys
import asyncio
from pathlib import Path

# Aggiungi il path del progetto
sys.path.append(str(Path(__file__).parent))

from src.config import Config
from src.ai import AudioAnalyzer

async def test_ai_analyzer():
    """Test dell'analyzer AI"""
    print("🧪 Test AudioAnalyzer...")
    
    try:
        analyzer = AudioAnalyzer()
        
        # Test analisi del tono con testo di esempio
        test_text = "Sono molto entusiasta di questo progetto! È fantastico vedere come l'intelligenza artificiale possa aiutarci a comprendere meglio le emozioni nelle conversazioni."
        
        print(f"📝 Testo di test: {test_text}")
        
        # Test analisi del tono
        tone_result = await analyzer.analyze_tone(test_text)
        print(f"🎭 Risultato analisi tono: {tone_result}")
        
        # Test riassunto
        summary_result = await analyzer.generate_summary(test_text)
        print(f"📋 Risultato riassunto: {summary_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test AI: {e}")
        return False

def test_config():
    """Test della configurazione"""
    print("🧪 Test Configurazione...")
    
    try:
        # Test validazione config
        Config.validate_config()
        print("✅ Configurazione valida")
        
        print(f"📁 Directory output: {Config.OUTPUT_DIR}")
        print(f"🎵 Sample rate: {Config.SAMPLE_RATE}")
        print(f"🔊 Canali: {Config.CHANNELS}")
        print(f"🎭 Analisi tono: {Config.TONE_ANALYSIS_ENABLED}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nella configurazione: {e}")
        return False

async def main():
    """Funzione principale di test"""
    print("🚀 Avvio test VibeTalking...\n")
    
    # Test configurazione
    config_ok = test_config()
    print()
    
    if config_ok:
        # Test AI analyzer
        ai_ok = await test_ai_analyzer()
        print()
        
        if ai_ok:
            print("✅ Tutti i test sono passati!")
            print("🎉 VibeTalking è pronto per l'uso!")
        else:
            print("❌ Test AI falliti - controlla la configurazione API")
    else:
        print("❌ Test configurazione falliti - controlla il file .env")

if __name__ == "__main__":
    asyncio.run(main())
