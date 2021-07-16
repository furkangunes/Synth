import numpy as np
from dataclasses import dataclass
from time import time

@dataclass
class Env:
    """
    Envelope to get better sound experience, mimic real instruments maybe
    """

    # TODO: Adjust timings
    attack_time = 0.5
    decay_time = 0.5
    sustain_amplitude: float
    release_time = 0.5

    start_time = time()

    def __call__(self, amplitude):
        now = time()

        if now < self.attack_time:
            return amplitude * (now - self.start_time) / self.attack_time
        elif now < self.decay_time:
            return amplitude * (1 - (now - self.start_time - self.attack_time) / self.decay_time)
        else:
            return self.sustain_amplitude

class Osc():
    """
    An oscillator to get more interesting sin waves
    """

    def __init__(self):
        self.active_function: self.sin_wave

    def sin_wave(self, phase, amplitude, f=0.0):
        # Return original sin wave
        return amplitude * np.sin(phase)

    def sqr_wave(self, phase, amplitude, f=0.0):
        # Return square shaped sin wave, which only alters between -1 and 1
        return amplitude * np.sign(np.sin(phase))

    def tri_wave(self, phase, amplitude, f=0.0):
        # Return triangular shaped sin wave, which forms a triangle over sin wave by its peak values
        return 2.0 * amplitude / np.pi * np.arcsin(self.sin_wave(phase, amplitude))

    def saw_wave(self, phase, amplitude, f):
        # Returns a saw tooth shaped cummulatively sampled sin waves
        if f == 0.0:
            return 0.0

        t = phase / (2.0 * np.pi * f)

        return 2.0 * amplitude / np.pi * (f * np.pi * (t % (1.0 / f)) - np.pi / 2.0)

    def __call__(self, phase, amplitude, f=0.0):
        # Call object directly with phase and amplitude (osc = Osc(); osc(phase, amplitude))
        return self.active_function(phase, amplitude, f)