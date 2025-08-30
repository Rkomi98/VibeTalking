"""
Visualizzatore dinamico del tono con animazioni
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib
import cairo
import math
import time
from typing import Dict, Optional

class ToneVisualizer(Gtk.DrawingArea):
    """Widget per visualizzare il tono con animazioni dinamiche"""
    
    def __init__(self):
        super().__init__()
        
        # Stato corrente
        self.current_tone = "neutrale"
        self.intensity = 0.5  # 0.0 - 1.0
        self.confidence = 0.5  # 0.0 - 1.0
        self.animation_time = 0.0
        self.is_recording = False
        
        # Colori per i diversi toni
        self.tone_colors = {
            "entusiasta": (1.0, 0.6, 0.0),      # Arancione caldo
            "felice": (1.0, 0.8, 0.0),          # Giallo
            "calmo": (0.0, 0.7, 1.0),           # Blu chiaro
            "neutrale": (0.5, 0.5, 0.5),        # Grigio
            "preoccupato": (0.8, 0.4, 0.0),     # Arancione scuro
            "arrabbiato": (1.0, 0.2, 0.2),      # Rosso
            "triste": (0.3, 0.3, 0.8),          # Blu scuro
            "eccitato": (1.0, 0.0, 1.0),        # Magenta
        }
        
        # Configura il widget
        self.set_size_request(300, 300)
        self.connect("draw", self.on_draw)
        
        # Timer per l'animazione
        self.animation_timer = GLib.timeout_add(50, self.update_animation)
        
    def update_tone(self, tone_data: Optional[Dict]):
        """Aggiorna il tono visualizzato"""
        if tone_data:
            self.current_tone = tone_data.get("tono_principale", "neutrale")
            
            # Converti intensità in valore numerico
            intensity_map = {"bassa": 0.3, "media": 0.6, "alta": 0.9}
            self.intensity = intensity_map.get(tone_data.get("intensità", "media"), 0.6)
            
            # Confidenza
            self.confidence = tone_data.get("confidenza", 50) / 100.0
            
            print(f"🎨 Tono aggiornato: {self.current_tone} (intensità: {self.intensity:.1f})")
        
        self.queue_draw()
    
    def set_recording_state(self, is_recording: bool):
        """Imposta lo stato di registrazione"""
        self.is_recording = is_recording
        self.queue_draw()
    
    def update_animation(self):
        """Aggiorna l'animazione"""
        self.animation_time += 0.1
        if self.animation_time > 2 * math.pi:
            self.animation_time = 0.0
        
        self.queue_draw()
        return True  # Continua l'animazione
    
    def on_draw(self, widget, cr):
        """Disegna la visualizzazione del tono"""
        # Ottieni dimensioni
        allocation = widget.get_allocation()
        width = allocation.width
        height = allocation.height
        center_x = width / 2
        center_y = height / 2
        
        # Sfondo
        cr.set_source_rgb(0.1, 0.1, 0.1)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        
        if self.is_recording:
            self._draw_recording_visualization(cr, center_x, center_y, width, height)
        else:
            self._draw_idle_state(cr, center_x, center_y, width, height)
        
        return False
    
    def _draw_recording_visualization(self, cr, center_x, center_y, width, height):
        """Disegna la visualizzazione durante la registrazione"""
        # Ottieni colore del tono corrente
        color = self.tone_colors.get(self.current_tone, (0.5, 0.5, 0.5))
        
        # Raggio base
        base_radius = min(width, height) * 0.3
        
        # Animazione pulsante basata sull'intensità
        pulse = math.sin(self.animation_time * 3) * 0.2 + 1.0
        animated_radius = base_radius * pulse * self.intensity
        
        # Cerchio principale (tono)
        cr.set_source_rgba(color[0], color[1], color[2], 0.8)
        cr.arc(center_x, center_y, animated_radius, 0, 2 * math.pi)
        cr.fill()
        
        # Cerchio interno (confidenza)
        confidence_radius = animated_radius * self.confidence
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.6)
        cr.arc(center_x, center_y, confidence_radius, 0, 2 * math.pi)
        cr.fill()
        
        # Onde concentriche
        for i in range(3):
            wave_radius = base_radius * (1.5 + i * 0.3)
            wave_alpha = 0.3 * math.sin(self.animation_time * 2 - i * 0.5)
            if wave_alpha > 0:
                cr.set_source_rgba(color[0], color[1], color[2], wave_alpha)
                cr.arc(center_x, center_y, wave_radius, 0, 2 * math.pi)
                cr.stroke()
        
        # Particelle fluttuanti per intensità alta
        if self.intensity > 0.7:
            self._draw_particles(cr, center_x, center_y, color)
        
        # Testo del tono
        self._draw_tone_text(cr, center_x, center_y + base_radius + 40)
    
    def _draw_idle_state(self, cr, center_x, center_y, width, height):
        """Disegna lo stato di riposo"""
        # Cerchio grigio statico
        radius = min(width, height) * 0.2
        cr.set_source_rgba(0.3, 0.3, 0.3, 0.8)
        cr.arc(center_x, center_y, radius, 0, 2 * math.pi)
        cr.fill()
        
        # Bordo
        cr.set_source_rgba(0.5, 0.5, 0.5, 1.0)
        cr.arc(center_x, center_y, radius, 0, 2 * math.pi)
        cr.stroke()
        
        # Testo
        cr.set_source_rgba(0.7, 0.7, 0.7, 1.0)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(14)
        
        text = "Premi per registrare"
        text_extents = cr.text_extents(text)
        cr.move_to(center_x - text_extents.width / 2, center_y + text_extents.height / 2)
        cr.show_text(text)
    
    def _draw_particles(self, cr, center_x, center_y, color):
        """Disegna particelle animate per alta intensità"""
        for i in range(8):
            angle = (self.animation_time + i * math.pi / 4) % (2 * math.pi)
            distance = 80 + math.sin(self.animation_time * 2 + i) * 20
            
            x = center_x + math.cos(angle) * distance
            y = center_y + math.sin(angle) * distance
            
            particle_alpha = 0.5 + math.sin(self.animation_time * 3 + i) * 0.3
            cr.set_source_rgba(color[0], color[1], color[2], particle_alpha)
            cr.arc(x, y, 3, 0, 2 * math.pi)
            cr.fill()
    
    def _draw_tone_text(self, cr, center_x, text_y):
        """Disegna il testo del tono corrente"""
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.9)
        cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(16)
        
        # Tono principale
        tone_text = f"Tono: {self.current_tone.title()}"
        text_extents = cr.text_extents(tone_text)
        cr.move_to(center_x - text_extents.width / 2, text_y)
        cr.show_text(tone_text)
        
        # Intensità e confidenza
        cr.set_font_size(12)
        cr.set_source_rgba(0.8, 0.8, 0.8, 0.8)
        
        stats_text = f"Intensità: {self.intensity:.1f} | Confidenza: {self.confidence:.0%}"
        text_extents = cr.text_extents(stats_text)
        cr.move_to(center_x - text_extents.width / 2, text_y + 25)
        cr.show_text(stats_text)
