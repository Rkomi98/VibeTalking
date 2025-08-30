"""
Modulo per l'analisi AI dell'audio utilizzando datapizzai
"""
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datapizzai import DataPizzaAI
from ..config import Config

class AudioAnalyzer:
    """Classe per l'analisi dell'audio con AI"""
    
    def __init__(self):
        self.client = DataPizzaAI(api_key=Config.GOOGLE_API_KEY)
        
    async def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """Trascrivi un file audio in testo"""
        try:
            print("🔄 Avvio trascrizione...")
            
            # Usa datapizzai per la trascrizione
            result = await self.client.transcribe_audio(
                audio_file=audio_file_path,
                language="it"  # Italiano
            )
            
            if result and 'text' in result:
                transcription = result['text']
                print(f"✅ Trascrizione completata: {len(transcription)} caratteri")
                return transcription
            else:
                print("❌ Nessun testo trascritto")
                return None
                
        except Exception as e:
            print(f"❌ Errore nella trascrizione: {e}")
            return None
    
    async def analyze_tone(self, text: str) -> Optional[Dict]:
        """Analizza il tono del testo trascritto"""
        if not text:
            return None
            
        try:
            print("🔄 Avvio analisi del tono...")
            
            # Prompt per l'analisi del tono
            prompt = f"""
            Analizza il tono e l'emozione del seguente testo trascritto da audio.
            
            Testo: "{text}"
            
            Fornisci un'analisi strutturata in formato JSON con:
            1. tono_principale: (entusiasta, neutrale, preoccupato, arrabbiato, felice, triste, calmo, eccitato)
            2. intensità: (bassa, media, alta) 
            3. confidenza: (percentuale da 0 a 100)
            4. emozioni_secondarie: (lista di emozioni aggiuntive rilevate)
            5. descrizione: (breve descrizione del tono rilevato)
            6. suggerimenti: (consigli per migliorare la comunicazione)
            
            Rispondi SOLO con il JSON, senza altro testo.
            """
            
            response = await self.client.generate_text(
                prompt=prompt,
                model="gemini-2.0-flash-exp"
            )
            
            if response:
                # Prova a parsare la risposta come JSON
                import json
                try:
                    tone_analysis = json.loads(response)
                    print("✅ Analisi del tono completata")
                    return tone_analysis
                except json.JSONDecodeError:
                    # Se non è JSON valido, crea una struttura di fallback
                    print("⚠️ Risposta non in formato JSON, creo analisi di fallback")
                    return {
                        "tono_principale": "neutrale",
                        "intensità": "media",
                        "confidenza": 50,
                        "emozioni_secondarie": [],
                        "descrizione": "Analisi automatica non disponibile",
                        "suggerimenti": ["Riprova con un audio più chiaro"]
                    }
            else:
                print("❌ Nessuna risposta dall'AI")
                return None
                
        except Exception as e:
            print(f"❌ Errore nell'analisi del tono: {e}")
            return None
    
    async def generate_summary(self, text: str) -> Optional[str]:
        """Genera un riassunto del testo trascritto"""
        if not text:
            return None
            
        try:
            print("🔄 Generazione riassunto...")
            
            prompt = f"""
            Crea un riassunto conciso e ben strutturato del seguente testo trascritto da audio.
            
            Testo: "{text}"
            
            Il riassunto deve:
            - Essere lungo massimo 3-4 frasi
            - Catturare i punti principali
            - Essere scritto in italiano
            - Essere chiaro e professionale
            """
            
            summary = await self.client.generate_text(
                prompt=prompt,
                model="gemini-2.0-flash-exp"
            )
            
            if summary:
                print("✅ Riassunto generato")
                return summary.strip()
            else:
                print("❌ Impossibile generare il riassunto")
                return None
                
        except Exception as e:
            print(f"❌ Errore nella generazione del riassunto: {e}")
            return None
    
    async def full_analysis(self, audio_file_path: str) -> Dict:
        """Esegue l'analisi completa di un file audio"""
        print(f"🎯 Avvio analisi completa di: {audio_file_path}")
        
        results = {
            "file_path": audio_file_path,
            "transcription": None,
            "tone_analysis": None,
            "summary": None,
            "timestamp": None
        }
        
        # Trascrizione
        transcription = await self.transcribe_audio(audio_file_path)
        results["transcription"] = transcription
        
        if transcription:
            # Analisi del tono
            if Config.TONE_ANALYSIS_ENABLED:
                tone_analysis = await self.analyze_tone(transcription)
                results["tone_analysis"] = tone_analysis
            
            # Riassunto
            summary = await self.generate_summary(transcription)
            results["summary"] = summary
        
        # Timestamp
        from datetime import datetime
        results["timestamp"] = datetime.now().isoformat()
        
        print("🎉 Analisi completa terminata")
        return results
    
    def save_analysis_results(self, results: Dict, output_file: Optional[str] = None) -> str:
        """Salva i risultati dell'analisi in un file JSON"""
        import json
        from datetime import datetime
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = Config.OUTPUT_DIR / f"analysis_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Risultati salvati in: {output_file}")
            return str(output_file)
            
        except Exception as e:
            print(f"❌ Errore nel salvataggio: {e}")
            return ""
