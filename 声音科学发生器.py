import numpy as np
import tkinter as tk
from tkinter import ttk
import tempfile
import scipy.io.wavfile
import platform
import os
from pygame import mixer  # NOTE: Using pygame for cross-platform audio playback

# NOTE: Detect platform for audio handling
WINDOWS = platform.system().lower() == 'windows'

# NOTE: Global variable to track active sounds for stop functionality
active_sounds = []

def generate_tone(frequency, duration=0.5, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def play_scale(scale_binary, base_frequency=440):
    global active_sounds
    scale_binary = str(scale_binary)
    semitone_ratio = 2 ** (1 / 12)
    scale_notes = []

    # NOTE: Clear previous sounds before playing new ones
    for sound in active_sounds:
        sound.stop()
    active_sounds.clear()

    for i, bit in enumerate(scale_binary):
        if bit == "1":
            scale_notes.append(base_frequency * (semitone_ratio ** i))

    # NOTE: Modified to allow scale_binary modification during playback
    for frequency in scale_notes:
        wave_data = generate_tone(frequency)
        
        # NOTE: Windows audio handling requires explicit file closing
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
            scipy.io.wavfile.write(tmpfile.name, 44100,
                                  (wave_data * 32767).astype(np.int16))
            if WINDOWS:
                tmpfile.close()  # NOTE: Required for Windows file handling
            
            mixer.init()
            sound = mixer.Sound(tmpfile.name)
            active_sounds.append(sound)  # Keep reference to prevent GC
            sound.play()
            
            if WINDOWS and tmpfile.name:
                os.unlink(tmpfile.name)  # NOTE: Manual cleanup for Windows

class ScalePlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scale Player")
        self.root.geometry("400x300")
        
        # NOTE: Initialize pygame mixer
        mixer.init()
        
        # NOTE: Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # NOTE: Input field for binary pattern
        self.input_label = ttk.Label(self.main_frame, text="Binary Pattern:")
        self.input_label.pack()
        
        self.input_field = ttk.Entry(self.main_frame, font=('Arial', 14))
        self.input_field.insert(0, '1000')
        self.input_field.pack(fill=tk.X, pady=5)
        
        # NOTE: Duration input
        self.duration_label = ttk.Label(self.main_frame, text="Duration (seconds):")
        self.duration_label.pack()
        
        self.duration_input = ttk.Entry(self.main_frame, font=('Arial', 14))
        self.duration_input.insert(0, '0.5')
        self.duration_input.pack(fill=tk.X, pady=5)
        
        # NOTE: Base frequency input
        self.freq_label = ttk.Label(self.main_frame, text="Base Frequency (Hz):")
        self.freq_label.pack()
        
        self.freq_input = ttk.Entry(self.main_frame, font=('Arial', 14))
        self.freq_input.insert(0, '440')
        self.freq_input.pack(fill=tk.X, pady=5)
        
        # NOTE: Play button triggers audio generation
        self.play_button = ttk.Button(
            self.main_frame,
            text="Play Scale",
            command=self.on_play_button
        )
        self.play_button.pack(fill=tk.X, pady=5)
        
        # NOTE: Stop button to interrupt playback
        self.stop_button = ttk.Button(
            self.main_frame,
            text="Stop",
            command=self.on_stop_button
        )
        self.stop_button.pack(fill=tk.X, pady=5)
    
    def on_play_button(self):
        # NOTE: Get all parameters and play scale with current settings
        try:
            duration = float(self.duration_input.get())
            base_freq = float(self.freq_input.get())
            scale_binary = self.input_field.get()
            
            # NOTE: Directly call play_scale without scheduling
            play_scale(scale_binary, base_freq)
        except ValueError:
            pass
    
    def on_stop_button(self):
        global active_sounds
        # NOTE: Stop all currently playing sounds
        for sound in active_sounds:
            sound.stop()
        active_sounds.clear()

if __name__ == "__main__":
    # NOTE: Main entry point launches Tkinter application
    root = tk.Tk()
    app = ScalePlayerApp(root)
    root.mainloop()
