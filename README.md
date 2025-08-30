<div align="center">

# 🎤 VibeTalking — DataPizza Console Edition

[![Stars](https://img.shields.io/github/stars/Rkomi98/VibeTalking?style=for-the-badge)](https://github.com/Rkomi98/VibeTalking/stargazers)
[![Forks](https://img.shields.io/github/forks/Rkomi98/VibeTalking?style=for-the-badge)](https://github.com/Rkomi98/VibeTalking/network/members)
[![Issues](https://img.shields.io/github/issues/Rkomi98/VibeTalking?style=for-the-badge)](https://github.com/Rkomi98/VibeTalking/issues)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](#)

<br/>

<img src="https://img.shields.io/badge/Powered%20by-DataPizzaAI%20%26%20Gemini%202.0%20Flash-ff69b4?style=for-the-badge" />

<br/>

<p>
VibeTalking è un'app console che registra audio dal microfono (arecord/ALSA) e lo analizza con una pipeline <b>DataPizzaAI</b> sfruttando <b>Gemini 2.0 Flash</b>:
<b>Trascrizione → Analisi del tono → Riassunto</b>. Zero crash, esperienza liscia su Linux.
</p>

</div>

---

## ✨ Caratteristiche

- 🎙️ Registrazione microfono reale (arecord/ALSA) o fallback demo
- 🧠 Pipeline DataPizza: MediaBlock + GoogleClient (Gemini 2.0 Flash)
- 📝 Trascrizione, 🎭 Analisi del tono, 📋 Riassunto
- 💾 Output JSON in `recordings/`
- 🐧 Versione console stabile (nessun XCB crash)

---

## 🚀 Avvio Rapido

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# (Facoltativo) API Key Gemini
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Avvio
python main_console.py
```

Suggerimento: se il microfono non è quello giusto, imposta la scheda ALSA prima di avviare:
```bash
arecord -l   # lista dispositivi
export ALSA_PCM_CARD=1
export ALSA_PCM_DEVICE=0
```

---

## 🧩 Architettura

- `main_console.py` — entrypoint console e UX
- `src/audio/` — backend audio (arecord, demo; selezione automatica)
- `src/ai/datapizza_analyzer.py` — pipeline DataPizza (MediaBlock → Trascrizione → Tono → Riassunto)
- `src/config.py` — configurazione e variabili ambiente

Pipeline DataPizza (semplificata):
```
WAV → MediaBlock → GoogleClient(Gemini 2.0 Flash)
→ Trascrizione (TextBlock)
→ Analisi Tono (JSON)
→ Riassunto (Text)
→ JSON su disco
```

---

## 📄 Output

Esempio JSON in `recordings/datapizza_analysis_*.json`:
```json
{
  "file_path": "recordings/recording_20250830_151539.wav",
  "transcription": "...",
  "tone_analysis": {
    "tono_principale": "neutrale",
    "intensità": "media",
    "confidenza": 82,
    "emozioni_secondarie": ["calmo"],
    "descrizione": "Tono equilibrato",
    "suggerimenti": ["Mantieni questo ritmo"]
  },
  "summary": "...",
  "timestamp": "2025-08-30T15:17:01.378789",
  "analyzer": "datapizzai"
}
```

---

## 🛠️ Troubleshooting

- Nessun audio/voce: 
  - `arecord -l` e imposta `ALSA_PCM_CARD`/`ALSA_PCM_DEVICE`
  - verifica permessi su dispositivi audio (`/dev/snd/*`)
- Niente API key: funziona lo stesso (fallback)
- Network/API error: fallback automatico al locale

---

## 🙌 Contribuire

1. Fai un fork del repo
2. Crea un branch feature: `git checkout -b feat/xyz`
3. Invia una PR

Se ti piace il progetto, lascia una ⭐ e fai un fork!

---

<div align="center">

Con amore per l'Audio + AI 💜

[![Stars](https://img.shields.io/github/stars/mcalcaterra/VibeTalking?style=social)](https://github.com/mcalcaterra/VibeTalking/stargazers)
[![Forks](https://img.shields.io/github/forks/mcalcaterra/VibeTalking?style=social)](https://github.com/mcalcaterra/VibeTalking/network/members)

</div>
