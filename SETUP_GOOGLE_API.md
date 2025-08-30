# 🔧 Configurazione Google Speech-to-Text API

Per abilitare la trascrizione reale dell'audio, segui questi passaggi:

## 1. Crea un Progetto Google Cloud

1. Vai su [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuovo progetto o seleziona uno esistente
3. Annota l'ID del progetto

## 2. Abilita l'API Speech-to-Text

1. Nel menu laterale, vai su **API e servizi** > **Libreria**
2. Cerca "Cloud Speech-to-Text API"
3. Clicca su **Abilita**

## 3. Crea una API Key

1. Vai su **API e servizi** > **Credenziali**
2. Clicca su **+ Crea credenziali** > **Chiave API**
3. Copia la chiave generata
4. (Opzionale) Limita la chiave all'API Speech-to-Text per sicurezza

## 4. Configura l'Applicazione

Crea un file `.env` nella directory del progetto:

```bash
# .env
GOOGLE_API_KEY=la_tua_chiave_api_qui
```

## 5. Test della Configurazione

Esegui l'applicazione:

```bash
python main_demo.py
```

Se configurato correttamente, vedrai:
```
🔧 Modalità completa attiva - trascrizione reale con Google Speech-to-Text
```

## 🆓 Alternative Gratuite

Se non vuoi configurare Google Cloud, l'app funziona perfettamente in modalità demo con:
- Trascrizione simulata basata sulla durata
- Analisi del tono funzionante
- Tutte le altre funzionalità

## ⚠️ Risoluzione Problemi

### Errore 403 - API Disabilitata
```
Cloud Speech-to-Text API has not been used in project...
```
**Soluzione**: Abilita l'API nel Google Cloud Console

### Errore di Rete
```
Network is unreachable
```
**Soluzione**: Controlla la connessione internet

### API Key Non Valida
```
API key not valid
```
**Soluzione**: Verifica che la chiave sia corretta nel file `.env`

## 💰 Costi

- **Primi 60 minuti/mese**: Gratuiti
- **Oltre 60 minuti**: $0.006 per 15 secondi
- **Dettagli**: [Prezzi Google Speech-to-Text](https://cloud.google.com/speech-to-text/pricing)

## 🔒 Sicurezza

- Non condividere mai la tua API key
- Aggiungi `.env` al `.gitignore`
- Considera l'uso di limitazioni API per la chiave
