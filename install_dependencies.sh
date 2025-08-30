#!/bin/bash
# Script per installare le dipendenze su Fedora

echo "🔧 Installazione dipendenze per VibeTalking su Fedora..."

# Aggiorna il sistema
echo "📦 Aggiornamento pacchetti di sistema..."
sudo dnf update -y

# Installa le dipendenze di sistema per audio e GUI
echo "🎵 Installazione dipendenze audio e GUI..."
sudo dnf install -y \
    python3-devel \
    python3-pip \
    portaudio-devel \
    gtk3-devel \
    gobject-introspection-devel \
    cairo-devel \
    cairo-gobject-devel \
    pulseaudio-libs-devel \
    alsa-lib-devel

# Installa PyGObject (GTK bindings per Python)
echo "🖼️ Installazione PyGObject..."
sudo dnf install -y python3-gobject python3-cairo

# Installa le dipendenze Python
echo "🐍 Installazione dipendenze Python..."
uv pip install -r requirements.txt

# Installa PyAudio separatamente (spesso problematico)
echo "🎤 Installazione PyAudio..."
uv pip install pyaudio

echo "✅ Installazione completata!"
echo "💡 Ora puoi creare il file .env con la tua GOOGLE_API_KEY"
echo "🚀 Esegui: python main.py"
