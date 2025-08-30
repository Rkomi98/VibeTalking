"""
Modulo per l'analisi AI dell'audio utilizzando datapizzai con MediaBlock e Pipeline
"""
import asyncio
import json
import base64
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from datapizzai.clients.google_client import GoogleClient
from datapizzai.pipeline.functional_pipeline import FunctionalPipeline, Dependency
from datapizzai.type import Media, MediaBlock, TextBlock, ROLE
from datapizzai.memory import Memory
from datapizzai.core.models import PipelineComponent

from ..config import Config


class AudioToMediaBlockComponent(PipelineComponent):
    """Componente per convertire un file audio in MediaBlock"""
    
    def _run(self, audio_file_path: str) -> MediaBlock:
        """Converte un file audio in MediaBlock"""
        try:
            # Crea un oggetto Media per l'audio
            media = Media(
                media_type="audio",
                source_type="path", 
                source=audio_file_path,
                extension="wav"
            )
            
            # Crea il MediaBlock
            media_block = MediaBlock(media=media)
            
            print(f"✅ Audio convertito in MediaBlock: {audio_file_path}")
            return media_block
            
        except Exception as e:
            print(f"❌ Errore nella conversione audio: {e}")
            raise
    
    async def _a_run(self, audio_file_path: str) -> MediaBlock:
        """Versione asincrona"""
        return self._run(audio_file_path)


class AudioTranscriptionComponent(PipelineComponent):
    """Componente per la trascrizione audio usando GoogleClient"""
    
    def __init__(self, google_client: GoogleClient):
        self.google_client = google_client
    
    def _run(self, media_block: MediaBlock) -> TextBlock:
        """Trascrivi l'audio nel MediaBlock"""
        try:
            print("🔄 Avvio trascrizione con Gemini...")
            
            # Prepara il prompt per la trascrizione
            prompt = "Trascrivi questo audio in italiano. Fornisci solo il testo trascritto senza commenti aggiuntivi."
            
            # Crea la memoria con il MediaBlock
            memory = Memory()
            memory.add_turn([media_block], ROLE.USER)
            
            # Esegui la trascrizione
            response = self.google_client.invoke(
                input=prompt,
                memory=memory
            )
            
            # Estrai il testo dalla risposta
            if response.content and len(response.content) > 0:
                first_block = response.content[0]
                if isinstance(first_block, TextBlock):
                    transcription = first_block.content
                    print(f"✅ Trascrizione completata: {len(transcription)} caratteri")
                    return TextBlock(content=transcription)
            
            # Fallback se non c'è risposta
            print("⚠️ Nessuna trascrizione ricevuta, uso fallback")
            fallback_text = "Trascrizione non disponibile - modalità demo attiva"
            return TextBlock(content=fallback_text)
            
        except Exception as e:
            print(f"⚠️ Errore nella trascrizione: {e}")
            # Fallback in caso di errore
            fallback_text = "Trascrizione non disponibile - errore nella connessione"
            return TextBlock(content=fallback_text)
    
    async def _a_run(self, media_block: MediaBlock) -> TextBlock:
        """Versione asincrona"""
        return await asyncio.to_thread(self._run, media_block)


class ToneAnalysisComponent(PipelineComponent):
    """Componente per l'analisi del tono usando GoogleClient"""
    
    def __init__(self, google_client: GoogleClient):
        self.google_client = google_client
    
    def _run(self, text_block: TextBlock) -> Dict:
        """Analizza il tono del testo"""
        try:
            print("🔄 Avvio analisi del tono con Gemini...")
            
            text = text_block.content
            
            # Prompt strutturato per l'analisi del tono
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
            
            Rispondi SOLO con il JSON valido, senza altro testo.
            """
            
            # Esegui l'analisi
            response = self.google_client.invoke(input=prompt)
            
            if response.content and len(response.content) > 0:
                first_block = response.content[0]
                if isinstance(first_block, TextBlock):
                    try:
                        # Prova a parsare come JSON
                        tone_analysis = json.loads(first_block.content)
                        print("✅ Analisi del tono completata")
                        return tone_analysis
                    except json.JSONDecodeError:
                        print("⚠️ Risposta non in formato JSON, uso fallback")
            
            # Fallback con analisi semplificata
            return self._fallback_tone_analysis(text)
            
        except Exception as e:
            print(f"⚠️ Errore nell'analisi del tono: {e}")
            return self._fallback_tone_analysis(text_block.content)
    
    def _fallback_tone_analysis(self, text: str) -> Dict:
        """Analisi del tono di fallback basata su parole chiave"""
        text_lower = text.lower()
        
        # Parole chiave per diversi toni
        tone_keywords = {
            "entusiasta": ["fantastico", "eccellente", "meraviglioso", "incredibile"],
            "felice": ["felice", "contento", "soddisfatto", "bene", "ottimo"],
            "calmo": ["tranquillo", "calmo", "sereno", "neutrale"],
            "preoccupato": ["preoccupato", "ansioso", "problema", "difficile"],
            "arrabbiato": ["arrabbiato", "irritato", "sbagliato", "errore"],
            "triste": ["triste", "deluso", "male", "peccato"],
        }
        
        # Conta occorrenze
        tone_scores = {}
        for tone, keywords in tone_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            tone_scores[tone] = score
        
        # Determina il tono principale
        if max(tone_scores.values()) == 0:
            main_tone = "neutrale"
            confidence = 60
        else:
            main_tone = max(tone_scores, key=tone_scores.get)
            confidence = min(85, 60 + tone_scores[main_tone] * 10)
        
        return {
            "tono_principale": main_tone,
            "intensità": "media",
            "confidenza": confidence,
            "emozioni_secondarie": [],
            "descrizione": f"Tono rilevato: {main_tone}",
            "suggerimenti": ["Continua così", "Mantieni questo atteggiamento"]
        }
    
    async def _a_run(self, text_block: TextBlock) -> Dict:
        """Versione asincrona"""
        return await asyncio.to_thread(self._run, text_block)


class SummaryComponent(PipelineComponent):
    """Componente per la generazione del riassunto usando GoogleClient"""
    
    def __init__(self, google_client: GoogleClient):
        self.google_client = google_client
    
    def _run(self, text_block: TextBlock) -> str:
        """Genera un riassunto del testo"""
        try:
            print("🔄 Generazione riassunto con Gemini...")
            
            text = text_block.content
            
            prompt = f"""
            Crea un riassunto conciso del seguente testo trascritto da audio.
            
            Testo: "{text}"
            
            Il riassunto deve:
            - Essere lungo massimo 2-3 frasi
            - Catturare i punti principali
            - Essere scritto in italiano
            - Essere chiaro e diretto
            
            Fornisci solo il riassunto, senza introduzioni.
            """
            
            response = self.google_client.invoke(input=prompt)
            
            if response.content and len(response.content) > 0:
                first_block = response.content[0]
                if isinstance(first_block, TextBlock):
                    summary = first_block.content.strip()
                    print("✅ Riassunto generato")
                    return summary
            
            # Fallback
            return self._fallback_summary(text)
            
        except Exception as e:
            print(f"⚠️ Errore nella generazione del riassunto: {e}")
            return self._fallback_summary(text_block.content)
    
    def _fallback_summary(self, text: str) -> str:
        """Riassunto di fallback semplificato"""
        sentences = text.split('.')
        if len(sentences) <= 2:
            return text
        else:
            # Prendi le prime 2 frasi
            return '. '.join(sentences[:2]).strip() + '.'
    
    async def _a_run(self, text_block: TextBlock) -> str:
        """Versione asincrona"""
        return await asyncio.to_thread(self._run, text_block)


class DataPizzaAudioAnalyzer:
    """Analyzer principale che usa datapizzai Pipeline"""
    
    def __init__(self):
        # Inizializza il client Google
        if Config.GOOGLE_API_KEY:
            try:
                self.google_client = GoogleClient(
                    api_key=Config.GOOGLE_API_KEY,
                    model="gemini-2.0-flash-exp",
                    temperature=0.3
                )
                self.demo_mode = False
                print("🔧 DataPizza modalità completa - Gemini 2.0 Flash")
            except Exception as e:
                print(f"⚠️ Errore inizializzazione GoogleClient: {e}")
                self.google_client = None
                self.demo_mode = True
                print("🔧 DataPizza modalità demo - fallback locale")
        else:
            self.google_client = None
            self.demo_mode = True
            print("🔧 DataPizza modalità demo - nessuna API key")
    
    async def analyze_audio_file(self, audio_file_path: str) -> Dict:
        """Analizza un file audio usando la pipeline datapizzai"""
        print(f"🎯 Avvio analisi DataPizza di: {audio_file_path}")
        
        try:
            # Crea la pipeline
            pipeline = FunctionalPipeline()
            
            # Componenti della pipeline
            audio_to_media = AudioToMediaBlockComponent()
            
            if self.google_client and not self.demo_mode:
                # Modalità completa con Gemini
                transcription_comp = AudioTranscriptionComponent(self.google_client)
                tone_comp = ToneAnalysisComponent(self.google_client)
                summary_comp = SummaryComponent(self.google_client)
            else:
                # Modalità demo con fallback
                transcription_comp = None
                tone_comp = None
                summary_comp = None
            
            # Esegui la pipeline step by step
            
            # Step 1: Converti audio in MediaBlock
            media_block = await audio_to_media.a_run(audio_file_path)
            
            # Step 2: Trascrizione
            if transcription_comp:
                text_block = await transcription_comp.a_run(media_block)
                transcription = text_block.content
            else:
                # Fallback locale
                transcription = self._get_demo_transcription(audio_file_path)
                text_block = TextBlock(content=transcription)
            
            # Step 3: Analisi del tono
            if tone_comp:
                tone_analysis = await tone_comp.a_run(text_block)
            else:
                # Fallback locale
                tone_analysis = self._get_demo_tone_analysis(transcription)
            
            # Step 4: Riassunto
            if summary_comp:
                summary = await summary_comp.a_run(text_block)
            else:
                # Fallback locale
                summary = self._get_demo_summary(transcription)
            
            # Risultato finale
            results = {
                "file_path": audio_file_path,
                "transcription": transcription,
                "tone_analysis": tone_analysis,
                "summary": summary,
                "timestamp": self._get_timestamp(),
                "analyzer": "datapizzai"
            }
            
            print("🎉 Analisi DataPizza completata")
            return results
            
        except Exception as e:
            print(f"❌ Errore nell'analisi DataPizza: {e}")
            # Fallback completo
            return self._get_fallback_results(audio_file_path)
    
    def _get_demo_transcription(self, audio_file_path: str) -> str:
        """Trascrizione demo basata sulla durata"""
        try:
            import wave
            with wave.open(audio_file_path, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                duration = frames / float(rate)
        except:
            duration = 15.0
        
        if duration < 10:
            return "Ciao, questo è un test di registrazione breve. Sto testando l'applicazione VibeTalking."
        elif duration < 30:
            return "Salve, questa è una registrazione di media durata. Sto parlando per testare le funzionalità dell'applicazione."
        else:
            return "Buongiorno, questa è una registrazione più lunga per testare le capacità dell'applicazione VibeTalking con datapizzai."
    
    def _get_demo_tone_analysis(self, text: str) -> Dict:
        """Analisi del tono demo"""
        return {
            "tono_principale": "neutrale",
            "intensità": "media",
            "confidenza": 70,
            "emozioni_secondarie": [],
            "descrizione": "Tono equilibrato (modalità demo)",
            "suggerimenti": ["Test completato con successo"]
        }
    
    def _get_demo_summary(self, text: str) -> str:
        """Riassunto demo"""
        sentences = text.split('.')
        if len(sentences) <= 2:
            return text
        return '. '.join(sentences[:2]).strip() + '.'
    
    def _get_timestamp(self) -> str:
        """Timestamp ISO"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _get_fallback_results(self, audio_file_path: str) -> Dict:
        """Risultati di fallback in caso di errore totale"""
        return {
            "file_path": audio_file_path,
            "transcription": "Trascrizione non disponibile",
            "tone_analysis": {
                "tono_principale": "neutrale",
                "intensità": "media", 
                "confidenza": 50,
                "emozioni_secondarie": [],
                "descrizione": "Analisi non disponibile",
                "suggerimenti": ["Riprova più tardi"]
            },
            "summary": "Riassunto non disponibile",
            "timestamp": self._get_timestamp(),
            "analyzer": "datapizzai-fallback"
        }
    
    def save_analysis_results(self, results: Dict, output_file: Optional[str] = None) -> str:
        """Salva i risultati dell'analisi in un file JSON"""
        from datetime import datetime
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = Config.OUTPUT_DIR / f"datapizza_analysis_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Risultati DataPizza salvati in: {output_file}")
            return str(output_file)
            
        except Exception as e:
            print(f"❌ Errore nel salvataggio: {e}")
            return ""
