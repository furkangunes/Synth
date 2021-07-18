import numpy as np
from dataclasses import dataclass
from time import time
from math import inf

from note import Note

class Env:
    """
    Envelope to get better sound experience, mimic real instruments maybe
    """

    def __init__(self, amplitude):
        self.attack_time = 0.01 # sec
        self.decay_time = 0.01 # sec
        self.sustain_amplitude = amplitude * 0.9
        self.release_time = 0.01 # sec

    def _on_press_amp(self, note: Note, time, amplitude):
        if time < note.press_time + self.attack_time:
            return amplitude * (time - note.press_time) / self.attack_time
        elif time < note.press_time + self.attack_time + self.decay_time:
            return amplitude - ((amplitude - self.sustain_amplitude) * (time - note.press_time - self.attack_time) / self.decay_time)
        else:
            return self.sustain_amplitude

    def __call__(self, note: Note, time, amplitude): # Amplitude is the max amp, a.k.a. volume
        if time > note.release_time:
            if time - note.release_time > self.release_time:
                note.release_time = inf
                note.is_active = False
                return 0.0

            if time >= note.press_time + self.attack_time + self.decay_time:
                return self.sustain_amplitude * (1.0 - (time - note.release_time) / self.release_time)
            return self._on_press_amp(note, time, amplitude) * (1.0 - (time - note.release_time) / self.release_time)

        return self._on_press_amp(note, time, amplitude)

class Osc():
    """
    An oscillator to get more interesting sin waves
    """

    @dataclass
    class Vibrato:
        amplitude = 0.001
        freq = 5.0
        is_active = False

        def __call__(self, freq, time): # freq is the carrier signal frequency
            if not self.is_active:
                return 0.0
            return self.amplitude * freq * np.sin(2.0 * np.pi * self.freq * time)

    def __init__(self):
        self.active_function: self.sin_wave
        self.vibrato = self.Vibrato()

    def _get_sin(self, freq, time):
        return np.sin(2.0 * np.pi * freq * time + self.vibrato(freq, time))

    def sin_wave(self, note, time, amplitude):
        # Return original sin wave
        return amplitude * self._get_sin(note.freq, time)

    def sqr_wave(self, note, time, amplitude):
        # Return square shaped sin wave, which only alters between -1 and 1
        return amplitude * np.sign(self._get_sin(note.freq, time))

    def tri_wave(self, note, time, amplitude):
        # Return triangular shaped sin wave, which forms a triangle over sin wave by its peak values
        return 2.0 * amplitude / np.pi * np.arcsin(self._get_sin(note.freq, time))

    def saw_wave(self, note, time, amplitude):
        # Returns a saw tooth shaped cummulatively sampled sin waves
        # Cannot use Vibrato for now
        if note.freq == 0.0:
            return 0.0

        return 2.0 * amplitude / np.pi * (note.freq * np.pi * (time % (1.0 / note.freq)) - np.pi / 2.0)

    def __call__(self, note, time, amplitude):
        # Call object directly with phase and amplitude (osc = Osc(); osc(phase, amplitude))
        return self.active_function(note, time, amplitude)
