import numpy as np
from dataclasses import dataclass
from time import time
from math import inf

from note import Note

class Env:
    """
    Envelope to get better sound experience, mimic real instruments maybe
    """

    def __init__(self, step_size, amplitude):
        # TODO: Adjust timings accourding to player timer
        self.attack_time = 0.5 * step_size
        self.decay_time = 0.5 * step_size
        self.sustain_amplitude = amplitude * 0.8
        self.release_time = 100 * step_size

    def __call__(self, note: Note, time, amplitude): # Amplitude is the max amp, a.k.a. volume
        if time > note.release_time:
            if time - note.release_time > self.release_time:
                note.release_time = inf
                return 0.0

            return self.sustain_amplitude * (1.0 - (time - note.release_time) / self.release_time)

        if time < note.press_time + self.attack_time:
            print("Attack")
            print()
            print("Time:", time)
            print("Press time:", note.press_time)
            print("Attack time:", self.attack_time)
            print()
            return amplitude * (time - note.press_time) / self.attack_time
        elif time < note.press_time + self.attack_time + self.decay_time:
            print("Decay")
            return amplitude * (1.0 - (time - note.press_time - self.attack_time) / self.decay_time)
        else:
            print("Sustain")
            return self.sustain_amplitude

class Osc():
    """
    An oscillator to get more interesting sin waves
    """

    def __init__(self):
        self.active_function: self.sin_wave

    def sin_wave(self, note, time, amplitude):
        # Return original sin wave
        return amplitude * np.sin(2.0 * np.pi * note.freq * time)

    def sqr_wave(self, note, time, amplitude):
        # Return square shaped sin wave, which only alters between -1 and 1
        return amplitude * np.sign(np.sin(2.0 * np.pi * note.freq * time))

    def tri_wave(self, note, time, amplitude):
        # Return triangular shaped sin wave, which forms a triangle over sin wave by its peak values
        return 2.0 * amplitude / np.pi * np.arcsin(np.sin(2.0 * np.pi * note.freq * time))

    def saw_wave(self, note, time, amplitude):
        # Returns a saw tooth shaped cummulatively sampled sin waves
        if note.freq == 0.0:
            return 0.0

        return 2.0 * amplitude / np.pi * (note.freq * np.pi * (time % (1.0 / note.freq)) - np.pi / 2.0)

    def __call__(self, note, time, amplitude):
        # Call object directly with phase and amplitude (osc = Osc(); osc(phase, amplitude))
        return self.active_function(note, time, amplitude)