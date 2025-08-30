# 🎤 VibeTalking - DataPizza Edition

## Panoramica

VibeTalking DataPizza Edition utilizza la libreria **datapizzai** per l'analisi audio avanzata con:

- **MediaBlock** per la gestione dell'audio
- **GoogleClient** con **Gemini 2.0 Flash** per trascrizione, analisi del tono e riassunto
- **Pipeline** strutturata per il processing dell'audio
- **Fallback intelligente** in caso di problemi API

## Caratteristiche

### 🔧 Tecnologie Utilizzate

- **datapizzai**: Framework per AI pipeline
- **Gemini 2.0 Flash**: Modello AI di Google per analisi multimodale
- **MediaBlock**: Gestione nativa dell'audio per AI
- **Pipeline Components**: Architettura modulare e scalabile

### 🎯 Funzionalità

1. **Registrazione Audio**: Supporto per audio reale (PyAudio) o simulato
2. **Trascrizione**: Gemini 2.0 Flash con fallback locale
3. **Analisi del Tono**: Rilevamento emozioni e suggerimenti
4. **Riassunto**: Sintesi automatica del contenuto
5. **Export JSON**: Risultati strutturati e persistenti

## Installazione

### Prerequisiti

```bash
# Crea ambiente virtuale
uv venv

# Attiva ambiente
source .venv/bin/activate

# Installa datapizzai (repository personalizzato)
uv pip install --extra-index-url https://pypi.fury.io/datapizzai/ datapizzai==3.0.8

# Installa dipendenze base
uv pip install python-dotenv
```

### Configurazione

1. **Crea file `.env`**:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

2. **Abilita Google AI Studio API** (opzionale):
   - Vai su [Google AI Studio](https://aistudio.google.com/)
   - Crea un progetto e ottieni l'API key
   - Inserisci la key nel file `.env`

## Utilizzo

### Avvio Applicazione

```bash
# Attiva ambiente virtuale
source .venv/bin/activate

# Avvia VibeTalking DataPizza Edition
python main_datapizza.py
```

### Interfaccia

- **🎤 Inizia Registrazione**: Avvia/ferma la registrazione audio
- **🔍 Analizza Audio**: Processa l'ultimo audio registrato
- **📋 Risultati**: Visualizza trascrizione, tono e riassunto

### Test Standalone

```bash
# Test del solo analyzer
python test_datapizza.py
```

## Architettura

### Pipeline DataPizza

```python
# 1. AudioToMediaBlockComponent
audio_file → MediaBlock

# 2. AudioTranscriptionComponent  
MediaBlock + Gemini → TextBlock (trascrizione)

# 3. ToneAnalysisComponent
TextBlock + Gemini → Dict (analisi tono)

# 4. SummaryComponent
TextBlock + Gemini → String (riassunto)
```

### Componenti Principali

- **`DataPizzaAudioAnalyzer`**: Orchestratore principale
- **`AudioToMediaBlockComponent`**: Conversione audio → MediaBlock
- **`AudioTranscriptionComponent`**: Trascrizione con Gemini
- **`ToneAnalysisComponent`**: Analisi emotiva
- **`SummaryComponent`**: Generazione riassunto

### Fallback System

1. **API Disponibile**: Usa Gemini 2.0 Flash per analisi completa
2. **API Non Disponibile**: Fallback locale con analisi semplificata
3. **Errore Totale**: Risultati di emergenza per continuità

## File di Output

### Struttura JSON

```json
{
  "file_path": "recordings/recording_20250830_142356.wav",
  "transcription": "Testo trascritto dall'audio...",
  "tone_analysis": {
    "tono_principale": "neutrale",
    "intensità": "media",
    "confidenza": 85,
    "emozioni_secondarie": ["calmo"],
    "descrizione": "Tono equilibrato e professionale",
    "suggerimenti": ["Mantieni questo atteggiamento"]
  },
  "summary": "Riassunto conciso del contenuto...",
  "timestamp": "2025-08-30T14:23:56.566766",
  "analyzer": "datapizzai"
}
```

### Directory Output

- **`recordings/`**: File audio WAV
- **`recordings/datapizza_analysis_*.json`**: Risultati analisi

## Modalità di Funzionamento

### 🔧 Modalità Completa (con API Key)

- Trascrizione reale con Gemini 2.0 Flash
- Analisi del tono avanzata
- Riassunto intelligente
- Supporto audio multimodale

### 🔧 Modalità Demo (senza API Key)

- Trascrizione simulata basata su durata
- Analisi del tono con parole chiave
- Riassunto semplificato
- Funzionalità complete offline

## Confronto con Versione Standard

| Caratteristica | Standard | DataPizza |
|---|---|---|
| **AI Framework** | Requests diretti | datapizzai Pipeline |
| **Modello AI** | Google Speech-to-Text | Gemini 2.0 Flash |
| **Gestione Audio** | File path | MediaBlock nativo |
| **Architettura** | Monolitica | Pipeline modulare |
| **Scalabilità** | Limitata | Alta (componenti) |
| **Fallback** | Semplice | Intelligente multi-livello |

## Vantaggi DataPizza

1. **🔧 Architettura Modulare**: Componenti riutilizzabili e testabili
2. **🎯 AI Nativo**: MediaBlock ottimizzato per contenuti multimodali
3. **🚀 Scalabilità**: Pipeline estendibili e parallelizzabili
4. **🛡️ Robustezza**: Fallback intelligenti e gestione errori
5. **📊 Tracing**: Monitoraggio automatico delle operazioni

## Troubleshooting

### Errori Comuni

1. **`ModuleNotFoundError: datapizzai`**
   ```bash
   uv pip install --extra-index-url https://pypi.fury.io/datapizzai/ datapizzai==3.0.8
   ```

2. **`GoogleClient initialization failed`**
   - Verifica `GOOGLE_API_KEY` nel file `.env`
   - L'app funziona comunque in modalità demo

3. **`Audio analysis failed`**
   - Controlla che il file audio esista
   - Usa il fallback automatico

### Debug

```bash
# Test configurazione
python -c "from src.config import Config; Config.validate_config()"

# Test analyzer
python test_datapizza.py

# Test completo
python main_datapizza.py
```

## Sviluppo

### Estendere la Pipeline

```python
class CustomAnalysisComponent(PipelineComponent):
    def _run(self, input_data):
        # Logica personalizzata
        return processed_data
    
    async def _a_run(self, input_data):
        return await asyncio.to_thread(self._run, input_data)
```

### Aggiungere Nuovi Modelli

```python
# In DataPizzaAudioAnalyzer.__init__
self.google_client = GoogleClient(
    api_key=Config.GOOGLE_API_KEY,
    model="gemini-2.0-flash-exp",  # Cambia modello
    temperature=0.3
)
```

---

**🎉 VibeTalking DataPizza Edition - Powered by datapizzai & Gemini 2.0 Flash**
