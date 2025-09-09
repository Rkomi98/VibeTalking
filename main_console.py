#!/usr/bin/env python3
"""
VibeTalking - Versione Console (Zero Crash)
Nessuna GUI, solo DataPizza + Gemini via terminale
"""
import asyncio
import sys
import time
from pathlib import Path

from src.config import Config
from src.audio import AudioRecorder
from src.ai.datapizza_analyzer import DataPizzaAudioAnalyzer


class VibeTalkingConsole:
    """VibeTalking versione console senza GUI"""
    
    def __init__(self):
        self.recorder = AudioRecorder()
        self.analyzer = DataPizzaAudioAnalyzer()
        
    def print_header(self):
        """Stampa header dell'applicazione"""
        print("\n" + "="*60)
        print("🎤 VibeTalking - DataPizza Console Edition")
        print("="*60)
        print("🔧 DataPizza + Gemini 2.0 Flash")
        print("🎯 MediaBlock + Pipeline + JSON Output")
        print("🐧 Linux Console - Zero Crash Guaranteed")
        print("="*60 + "\n")
    
    def print_menu(self):
        """Stampa menu opzioni"""
        print("📋 OPZIONI:")
        print("1️⃣  Registra Audio (3 secondi)")
        print("2️⃣  Registra Audio (10 secondi)")
        print("3️⃣  Registra Audio (30 secondi)")
        print("4️⃣  Registra fino a INVIO 🔴")
        print("5️⃣  Analizza Ultimo Audio")
        print("6️⃣  Mostra File Registrati")
        print("7️⃣  Test Completo (Registra + Analizza)")
        print("0️⃣  Esci")
        print("-" * 40)
    
    def record_audio(self, duration: int = None) -> str:
        """Registra audio per la durata specificata o fino a Invio"""
        if duration is None:
            print(f"\n🎤 REGISTRAZIONE CONTINUA")
            print("=" * 40)
            print("🔴 Premi INVIO per fermare la registrazione")
        else:
            print(f"\n🎤 Avvio registrazione ({duration} secondi)...")
        
        # Avvia registrazione
        recording_file = self.recorder.start_recording()
        if not recording_file:
            print("❌ Errore nell'avvio della registrazione")
            return ""
        
        print(f"✅ Registrazione avviata: {Path(recording_file).name}")
        
        if duration is None:
            # Registrazione continua fino a Invio
            print("🔴 Registrazione in corso... (premi INVIO per fermare)")
            print("📢 Parla ora!")
            
            import sys
            import select
            
            # Mostra timer in tempo reale
            start_time = time.time()
            try:
                while True:
                    elapsed = time.time() - start_time
                    print(f"\r⏱️  Registrando... {elapsed:.1f}s - Premi INVIO per fermare", end="", flush=True)
                    
                    # Controlla se è stato premuto Invio (Linux/Unix)
                    if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                        sys.stdin.readline()
                        break
                    
                    time.sleep(0.1)
                    
            except KeyboardInterrupt:
                print("\n⚠️ Interruzione utente (Ctrl+C)")
            
            elapsed_total = time.time() - start_time
            print(f"\n⏹️  Registrazione fermata dopo {elapsed_total:.1f}s")
            
        else:
            # Registrazione a durata fissa (modalità esistente)
            # Countdown
            for i in range(duration, 0, -1):
                print(f"⏳ {i}...", end=" ", flush=True)
                time.sleep(1)
            print("\n")
        
        # Ferma registrazione
        saved_file = self.recorder.stop_recording()
        if saved_file:
            file_size = Path(saved_file).stat().st_size
            print(f"✅ Registrazione completata!")
            print(f"📁 File: {Path(saved_file).name}")
            print(f"📊 Dimensione: {file_size:,} bytes")
            return saved_file
        else:
            print("❌ Errore nel salvataggio")
            return ""
    
    async def analyze_audio(self, audio_file: str):
        """Analizza un file audio"""
        if not audio_file or not Path(audio_file).exists():
            print("❌ File audio non trovato")
            return
        
        print(f"\n🔍 Avvio analisi DataPizza...")
        print(f"📁 File: {Path(audio_file).name}")
        
        try:
            # Analisi
            results = await self.analyzer.analyze_audio_file(audio_file)
            
            if not results:
                print("❌ Nessun risultato dall'analisi")
                return
            
            # Salva risultati
            output_file = self.analyzer.save_analysis_results(results)
            
            # Mostra risultati
            self.display_results(results, output_file)
            
        except Exception as e:
            print(f"❌ Errore nell'analisi: {e}")
    
    def display_results(self, results: dict, output_file: str):
        """Mostra i risultati dell'analisi"""
        print("\n" + "="*60)
        print("🎯 RISULTATI ANALISI DATAPIZZA")
        print("="*60)
        
        # Info file
        print(f"📁 File Audio: {Path(results.get('file_path', '')).name}")
        print(f"💾 Risultati JSON: {Path(output_file).name}")
        print(f"🔧 Analyzer: {results.get('analyzer', 'N/A')}")
        print(f"⏰ Timestamp: {results.get('timestamp', 'N/A')}")
        
        print("\n📝 TRASCRIZIONE:")
        print("-" * 30)
        transcription = results.get('transcription', 'N/A')
        print(f"'{transcription}'")
        
        print("\n🎭 ANALISI DEL TONO:")
        print("-" * 30)
        tone = results.get('tone_analysis', {})
        print(f"• Tono principale: {tone.get('tono_principale', 'N/A')}")
        print(f"• Intensità: {tone.get('intensità', 'N/A')}")
        print(f"• Confidenza: {tone.get('confidenza', 'N/A')}%")
        print(f"• Descrizione: {tone.get('descrizione', 'N/A')}")
        
        emotions = tone.get('emozioni_secondarie', [])
        if emotions:
            print(f"• Emozioni secondarie: {', '.join(emotions)}")
        
        suggestions = tone.get('suggerimenti', [])
        if suggestions:
            print("• Suggerimenti:")
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        
        print("\n📋 RIASSUNTO:")
        print("-" * 30)
        summary = results.get('summary', 'N/A')
        print(f"'{summary}'")
        
        print("\n" + "="*60)
        print("🎉 Analisi completata con DataPizzaAI!")
        print("="*60 + "\n")
    
    def show_recordings(self):
        """Mostra i file registrati"""
        recordings_dir = Path("recordings")
        if not recordings_dir.exists():
            print("❌ Directory recordings non trovata")
            return
        
        # File audio
        audio_files = list(recordings_dir.glob("recording_*.wav"))
        json_files = list(recordings_dir.glob("datapizza_analysis_*.json"))
        
        print(f"\n📁 FILE NELLA DIRECTORY recordings/:")
        print("-" * 40)
        
        if audio_files:
            print("🎵 FILE AUDIO:")
            for i, file in enumerate(sorted(audio_files)[-5:], 1):  # Ultimi 5
                size = file.stat().st_size
                print(f"  {i}. {file.name} ({size:,} bytes)")
        
        if json_files:
            print("\n📊 ANALISI JSON:")
            for i, file in enumerate(sorted(json_files)[-5:], 1):  # Ultimi 5
                print(f"  {i}. {file.name}")
        
        if not audio_files and not json_files:
            print("📂 Nessun file trovato")
        
        print()
    
    async def test_complete(self):
        """Test completo: registra + analizza"""
        print("\n🧪 TEST COMPLETO - Registrazione + Analisi")
        print("-" * 50)
        
        # Registra 5 secondi
        audio_file = self.record_audio(5)
        if not audio_file:
            return
        
        # Analizza
        await self.analyze_audio(audio_file)
    
    def get_latest_recording(self) -> str:
        """Ottieni l'ultimo file registrato"""
        recordings_dir = Path("recordings")
        if not recordings_dir.exists():
            return ""
        
        audio_files = list(recordings_dir.glob("recording_*.wav"))
        if not audio_files:
            return ""
        
        return str(sorted(audio_files)[-1])
    
    async def run(self):
        """Loop principale dell'applicazione"""
        self.print_header()
        
        while True:
            self.print_menu()
            
            try:
                choice = input("👉 Scegli opzione (0-7): ").strip()
                
                if choice == "0":
                    print("\n👋 Arrivederci!")
                    break
                
                elif choice == "1":
                    self.record_audio(3)
                
                elif choice == "2":
                    self.record_audio(10)
                
                elif choice == "3":
                    self.record_audio(30)
                
                elif choice == "4":
                    self.record_audio()  # Registrazione continua senza durata
                
                elif choice == "5":
                    latest = self.get_latest_recording()
                    if latest:
                        await self.analyze_audio(latest)
                    else:
                        print("❌ Nessun file audio trovato. Registra prima!")
                
                elif choice == "6":
                    self.show_recordings()
                
                elif choice == "7":
                    await self.test_complete()
                
                else:
                    print("❌ Opzione non valida")
                
                # Pausa prima del prossimo menu
                if choice != "0":
                    input("\n⏎ Premi INVIO per continuare...")
                    print("\n" * 2)
            
            except KeyboardInterrupt:
                print("\n\n👋 Interruzione utente - Arrivederci!")
                break
            except Exception as e:
                print(f"\n❌ Errore: {e}")
                input("\n⏎ Premi INVIO per continuare...")


async def main():
    """Funzione principale"""
    try:
        # Verifica configurazione
        Config.validate_config()
        
        # Avvia app console
        app = VibeTalkingConsole()
        await app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Chiusura...")
    except Exception as e:
        print(f"❌ Errore critico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
