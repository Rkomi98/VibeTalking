# 🎤 VibeTalking

**Applicazione di Registrazione Audio con Analisi del Tono AI per Fedora Linux**

VibeTalking è un'applicazione innovativa che registra l'audio durante meeting o sessioni di parlato, trascrive il contenuto e analizza il tono della voce utilizzando l'intelligenza artificiale. L'app include visualizzazioni dinamiche che cambiano in base al tono rilevato.

## ✨ Funzionalità

### 🎯 Funzionalità Base
- **Registrazione Audio**: Cattura audio dal microfono in tempo reale
- **Trascrizione Automatica**: Converte l'audio in testo utilizzando Gemini AI
- **Riassunto Intelligente**: Genera riassunti concisi delle registrazioni

### 🚀 Funzionalità Avanzate
- **Analisi del Tono**: Rileva e classifica il tono della voce (entusiasta, calmo, preoccupato, ecc.)
- **Visualizzazione Dinamica**: Animazioni grafiche che cambiano in base al tono rilevato
- **Interfaccia Moderna**: GUI nativa GTK ottimizzata per Fedora Linux
- **Salvataggio Automatico**: Salva registrazioni e analisi in formato JSON

## 🛠️ Tecnologie Utilizzate

- **Python 3.13+** - Linguaggio principale
- **GTK 3** - Interfaccia grafica nativa
- **DataPizzaAI** - Integrazione con Gemini AI per trascrizione e analisi
- **PyAudio** - Registrazione audio
- **Cairo** - Rendering grafico per le animazioni

## 📋 Requisiti di Sistema

- **OS**: Fedora Linux (testato su Fedora 42)
- **Python**: 3.13 o superiore
- **Audio**: PulseAudio o PipeWire
- **Memoria**: Minimo 4GB RAM
- **Spazio**: 500MB liberi

## 🚀 Installazione

### 1. Clona il Repository
```bash
git clone https://github.com/tuousername/VibeTalking.git
cd VibeTalking
```

### 2. Installa le Dipendenze
```bash
# Esegui lo script di installazione automatica
./install_dependencies.sh

# Oppure installa manualmente:
sudo dnf install python3-devel portaudio-devel gtk3-devel gobject-introspection-devel
uv pip install -r requirements.txt
```

### 3. Configura l'API Key (Opzionale)
Per la trascrizione reale, crea un file `.env` nella directory principale:
```bash
# .env
GOOGLE_API_KEY=la_tua_api_key_qui

# Configurazioni opzionali
DEFAULT_SAMPLE_RATE=44100
DEFAULT_CHANNELS=1
TONE_ANALYSIS_ENABLED=true
ANIMATION_ENABLED=true
OUTPUT_DIR=./recordings
```

**Nota**: Senza API key, l'app funziona in modalità demo con trascrizione simulata.

### 4. Avvia l'Applicazione
```bash
python main.py
```

## 🎮 Come Usare

1. **Avvia l'applicazione** con `python main.py`
2. **Premi "Inizia Registrazione"** per iniziare a registrare
3. **Parla normalmente** - vedrai la visualizzazione animata
4. **Premi "Ferma Registrazione"** quando hai finito
5. **Clicca "Analizza Ultimo"** per avviare l'analisi AI
6. **Visualizza i risultati** nell'area di testo in basso

## 🎨 Visualizzazione del Tono

L'applicazione mostra diverse visualizzazioni basate sul tono rilevato:

- **🟠 Entusiasta**: Animazioni calde con particelle fluttuanti
- **🔵 Calmo**: Onde blu rilassanti
- **🔴 Arrabbiato**: Pulsazioni rosse intense  
- **🟡 Felice**: Colori gialli brillanti
- **⚫ Neutrale**: Visualizzazione grigia statica

## 📁 Struttura del Progetto

```
VibeTalking/
├── main.py                 # Entry point dell'applicazione
├── src/
│   ├── config.py          # Configurazione
│   ├── audio/             # Moduli audio
│   │   └── recorder.py    # Registrazione audio
│   ├── ai/                # Moduli AI
│   │   └── analyzer.py    # Analisi con Gemini
│   ├── gui/               # Interfaccia grafica
│   │   ├── main_window.py # Finestra principale
│   │   └── tone_visualizer.py # Visualizzatore tono
│   └── utils/             # Utilità
├── recordings/            # Directory registrazioni
├── requirements.txt       # Dipendenze Python
└── install_dependencies.sh # Script installazione
```

## ⚙️ Configurazione Avanzata

### Personalizzare i Colori del Tono
Modifica il dizionario `tone_colors` in `src/gui/tone_visualizer.py`:

```python
self.tone_colors = {
    "entusiasta": (1.0, 0.6, 0.0),  # RGB personalizzato
    "calmo": (0.0, 0.7, 1.0),
    # ... altri toni
}
```

### Modificare la Qualità Audio
Nel file `.env`:
```bash
DEFAULT_SAMPLE_RATE=48000  # Qualità superiore
DEFAULT_CHANNELS=2         # Stereo
```

## 🐛 Risoluzione Problemi

### Errore PyAudio
```bash
sudo dnf install portaudio-devel
uv pip install --force-reinstall pyaudio
```

### Errore GTK
```bash
sudo dnf install gtk3-devel gobject-introspection-devel
```

### Errore API Key
- Verifica che il file `.env` esista
- Controlla che `GOOGLE_API_KEY` sia impostata correttamente
- Assicurati di avere crediti API disponibili

## 🤝 Contribuire

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 🙏 Ringraziamenti

- **DataPizza** per l'eccellente libreria AI
- **GTK Team** per il toolkit grafico
- **Gemini AI** per le capacità di analisi del linguaggio

---

**Sviluppato con ❤️ per la community Fedora Linux**
 An applcation for Fedora to transcribe what you say
