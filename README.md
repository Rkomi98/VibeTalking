<div align="left">

# VibeTalking
<!-- Repo status -->
[![Last commit](https://img.shields.io/github/last-commit/Rkomi98/VibeTalking?style=flat-square)](https://github.com/Rkomi98/VibeTalking/commits)
[![Issues](https://img.shields.io/github/issues-raw/Rkomi98/VibeTalking?style=flat-square)](https://github.com/Rkomi98/VibeTalking/issues)
[![PRs](https://img.shields.io/github/issues-pr-raw/Rkomi98/VibeTalking?style=flat-square)](https://github.com/Rkomi98/VibeTalking/pulls)
[![Repo size](https://img.shields.io/github/repo-size/Rkomi98/VibeTalking?style=flat-square)](#)
[![Stars](https://img.shields.io/github/stars/Rkomi98/VibeTalking?style=social)](https://github.com/Rkomi98/VibeTalking/stargazers)

<!-- Tech stack -->
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white&style=flat-square)](#)
[![ALSA](https://img.shields.io/badge/Audio-ALSA/arecord-ff69b4?style=flat-square)](#)
[![GTK optional](https://img.shields.io/badge/GUI-Opzionale_(console)-lightgrey?style=flat-square)](#)
[![AI](https://img.shields.io/badge/AI-Gemini_2.0_Flash_+_Ollama-4285F4?logo=google&logoColor=white&style=flat-square)](#)
[![DataPizzaAI](https://img.shields.io/badge/Lib-DataPizzaAI-8A2BE2?style=flat-square)](#)
[![Ollama](https://img.shields.io/badge/Local-Ollama_Gemma2-000000?logo=ollama&logoColor=white&style=flat-square)](#)
[![Requests](https://img.shields.io/badge/Lib-requests-5A9?style=flat-square)](#)
[![dotenv](https://img.shields.io/badge/Lib-python--dotenv-4B8BBE?style=flat-square)](#)

<img width="1024" height="1024" alt="immagine" src="https://github.com/user-attachments/assets/dbc69d4c-1ce9-4a60-a25f-508f47d0f9f8" />

Piccola app da terminale per registrare audio (o simularlo), inviarlo a una pipeline di analisi basata su DataPizza/Gemini e salvare tutto in JSON. Niente GUI: semplice, stabile, pronta per Linux.

</div>

---

## Caratteristiche

- Registrazione dal microfono via ALSA/arecord, con fallback demo.
- **Doppio supporto AI**: Gemini 2.0 Flash (cloud) o Ollama/Gemma3n (locale).
- **Cambio provider runtime**: scegli Gemini/Ollama/Demo direttamente nell'app.
- Pipeline DataPizza: MediaBlock → Trascrizione → Analisi tono → Riassunto.
- Output completo in JSON nella cartella `recordings/`.
- Funziona anche senza API key: attiva un fallback locale.

---

## Avvio rapido

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Configurazione AI (scegli una delle opzioni):

# Opzione 1: Gemini (cloud)
echo "AI_PROVIDER=gemini" > .env
echo "GOOGLE_API_KEY=la_tua_api_key" >> .env

# Opzione 2: Ollama (locale)
echo "AI_PROVIDER=ollama" > .env
echo "OLLAMA_BASE_URL=http://localhost:11434" >> .env
echo "OLLAMA_MODEL=gemma2:2b" >> .env

# avvio
python main_console.py
```

### Setup Ollama (opzionale)

Per usare Gemma3n localmente:
```bash
# Installa Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Scarica Gemma3n (o altri modelli)
ollama pull gemma3n:2b     # Leggero (1.6GB) - Default
ollama pull gemma2:9b      # Più potente (5.4GB)
ollama pull llama3.2:3b    # Alternativa

# Verifica che funzioni
ollama list
```

**💡 Tip**: Puoi cambiare provider direttamente nell'app con l'opzione "7️⃣ Cambia Provider AI" - non serve riavviare!

### Configurazione audio

Se il microfono non è quello giusto:
```bash
arecord -l   # elenca i dispositivi
export ALSA_PCM_CARD=1
export ALSA_PCM_DEVICE=0
```

Se `datapizzai` è su registry privato, configura l'accesso con `.netrc` o passa `--index-url/--extra-index-url` a `uv pip`.

---

## Architettura

- `main_console.py`: entrypoint e flusso da terminale.
- `src/audio/`: backend di registrazione (arecord reale, oppure demo).
- `src/ai/datapizza_analyzer.py`: pipeline DataPizza (Gemini) con fallback locale.
- `src/config.py`: configurazione e variabili d’ambiente.

Schema sintetico:
```
WAV → MediaBlock → AI Client (Gemini o Ollama)
→ Trascrizione (TextBlock)
→ Analisi del tono (JSON)
→ Riassunto (Text)
→ Salvataggio su disco
```

**Provider supportati:**
- **Gemini 2.0 Flash**: trascrizione audio nativa + analisi avanzata
- **Ollama/Gemma3n**: ⚠️ NO trascrizione reale (analisi durata/volume) + analisi testo locale
- **Demo Mode**: simulazione completa senza AI (per test)

> **Nota importante**: Ollama non supporta file audio. La "trascrizione" è basata su analisi delle caratteristiche del file (durata, volume) per generare testo realistico che Ollama può poi analizzare per tono e riassunto.

---

## Output

I risultati si trovano in `recordings/datapizza_analysis_*.json`. Contengono percorso del file audio, trascrizione, analisi del tono, riassunto, timestamp e il tipo di analyzer usato.

---

## Risoluzione problemi

- **Nessun audio registrato:**
  - `arecord -l` e imposta `ALSA_PCM_CARD` / `ALSA_PCM_DEVICE`.
  - verifica i permessi su `/dev/snd/*`.
- **Problemi Gemini:**
  - mancanza API key → parte il fallback locale.
  - errori di rete → fallback automatico.
- **Problemi Ollama:**
  - `ollama serve` non in esecuzione → avvia con `ollama serve`.
  - modello non trovato → scarica con `ollama pull gemma2:2b`.
  - porta diversa → imposta `OLLAMA_BASE_URL` nel `.env`.
- **`datapizzai` non si installa:**
  - è probabilmente su un registry privato. Usa `.netrc` o specifica l'index URL.

---

## Contribuire

1. Fork del repository
2. Branch dedicato: `git checkout -b feat/xyz`
3. Pull request

Se trovi utile il progetto, una ⭐ fa piacere.

---

<div align="center">
Fatto per Linux, con un’attenzione alla semplicità.
</div>
