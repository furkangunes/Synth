import numpy as np
import simpleaudio as sa
from threading import RLock

# calculate note frequencies
A_freq = 440
Csh_freq = A_freq * 2 ** (4 / 12)
E_freq = A_freq * 2 ** (7 / 12)

class Player:
    T = 0.5

    def __init__(self, num_channels = 1, bytes_per_sample = 2, sample_rate = 44100):
        self.num_channels = num_channels
        self.bytes_per_sample = bytes_per_sample
        self.sample_rate = sample_rate
        self.t = np.linspace(0, self.T, int(self.T * sample_rate), False)

    def wave_gen(self, freq, lock):
        while True:
            #with lock:
            wave = np.sin(freq[0] * self.t * 2 * np.pi)
            print("Thread:", freq)
            yield wave * 10000 #(32767 / np.max(np.abs(note))) * 0.1

    def play(self, freq, lock: RLock):
            for wave in self.wave_gen(freq, lock):
                wave = wave.astype(np.int16)

                # start playback
                play_obj = sa.play_buffer(wave, self.num_channels, self.bytes_per_sample, self.sample_rate)

                # wait for playback to finish before exiting
                play_obj.wait_done()