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

    def __call__(self, time, amplitude):
        if time < self.attack_time:
            return amplitude * (time - self.start_time) / self.attack_time
        elif time < self.decay_time:
            return amplitude * (1 - (time - self.start_time - self.attack_time) / self.decay_time)
        else:
            return self.sustain_amplitude

class Osc():
    """
    An oscillator to get more interesting sin waves
    """

    def __init__(self):
        self.active_function: self.sin_wave

    def sin_wave(self, notes, time, amplitude):
        # Return original sin wave
        return amplitude * sum(np.sin(2.0 * np.pi * note.freq * time) for note in notes)

    def sqr_wave(self, notes, time, amplitude):
        # Return square shaped sin wave, which only alters between -1 and 1
        return amplitude * sum(np.sign(np.sin(2.0 * np.pi * note.freq * time)) for note in notes)

    def tri_wave(self, notes, time, amplitude):
        # Return triangular shaped sin wave, which forms a triangle over sin wave by its peak values
        return 2.0 * amplitude / np.pi * sum(np.arcsin(np.sin(2.0 * np.pi * note.freq * time)) for note in notes)

    def saw_wave(self, notes, time, amplitude):
        # Returns a saw tooth shaped cummulatively sampled sin waves

        # Do explicit for loop to prevent possible div by zero
        val = 0.0
        for note in notes:
            if note.freq != 0.0:
               val += note.freq * np.pi * (time % (1.0 / note.freq)) - np.pi / 2.0

        return 2.0 * amplitude / np.pi * val

    def __call__(self, notes, time, amplitude):
        # Call object directly with phase and amplitude (osc = Osc(); osc(phase, amplitude))
        return self.active_function(notes, time, amplitude)