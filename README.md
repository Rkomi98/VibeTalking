<div align="left">

# VibeTalking — Console Edition

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
[![AI](https://img.shields.io/badge/AI-Gemini_2.0_Flash-4285F4?logo=google&logoColor=white&style=flat-square)](#)
[![DataPizzaAI](https://img.shields.io/badge/Lib-DataPizzaAI-8A2BE2?style=flat-square)](#)
[![Requests](https://img.shields.io/badge/Lib-requests-5A9?style=flat-square)](#)
[![dotenv](https://img.shields.io/badge/Lib-python--dotenv-4B8BBE?style=flat-square)](#)

Piccola app da terminale per registrare audio (o simularlo), inviarlo a una pipeline di analisi basata su DataPizza/Gemini e salvare tutto in JSON. Niente GUI: semplice, stabile, pronta per Linux.

</div>

---

## Caratteristiche

- Registrazione dal microfono via ALSA/arecord, con fallback demo.
- Pipeline DataPizza: MediaBlock → Trascrizione → Analisi tono → Riassunto.
- Output completo in JSON nella cartella `recordings/`.
- Funziona anche senza API key: attiva un fallback locale.

---

## Avvio rapido

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# (facoltativo) API key Gemini
echo "GOOGLE_API_KEY=la_tua_api_key" > .env

# avvio
python main_console.py
```

Se il microfono non è quello giusto, selezionalo così:
```bash
arecord -l   # elenca i dispositivi
export ALSA_PCM_CARD=1
export ALSA_PCM_DEVICE=0
```

Se `datapizzai` è su registry privato, configura l’accesso con `.netrc` o passa `--index-url/--extra-index-url` a `uv pip`.

---

## Architettura

- `main_console.py`: entrypoint e flusso da terminale.
- `src/audio/`: backend di registrazione (arecord reale, oppure demo).
- `src/ai/datapizza_analyzer.py`: pipeline DataPizza (Gemini) con fallback locale.
- `src/config.py`: configurazione e variabili d’ambiente.

Schema sintetico:
```
WAV → MediaBlock → GoogleClient (Gemini 2.0 Flash)
→ Trascrizione (TextBlock)
→ Analisi del tono (JSON)
→ Riassunto (Text)
→ Salvataggio su disco
```

---

## Output

I risultati si trovano in `recordings/datapizza_analysis_*.json`. Contengono percorso del file audio, trascrizione, analisi del tono, riassunto, timestamp e il tipo di analyzer usato.

---

## Risoluzione problemi

- Nessun audio registrato:
  - `arecord -l` e imposta `ALSA_PCM_CARD` / `ALSA_PCM_DEVICE`.
  - verifica i permessi su `/dev/snd/*`.
- Mancanza API key / problemi di rete:
  - parte il fallback locale (la pipeline restituisce comunque dati di test).
- `datapizzai` non si installa:
  - è probabilmente su un registry privato. Usa `.netrc` o specifica l’index URL.

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
