import tkinter as tk
import simpleaudio as sa
import threading
import numpy as np

# calculate note frequencies
A_freq = 440
Csh_freq = A_freq * 2 ** (4 / 12)
E_freq = A_freq * 2 ** (7 / 12)

sample_rate = 44100

def note_gen():
    T = 0.25
    t = np.linspace(0, T, int(T * sample_rate), False)

    i = 0
    while True:
        if i % 3 == 0:
            freq = A_freq
        elif i % 3 == 1:
            freq = Csh_freq
        else:
            freq = E_freq

        i += 1
        note = np.sin(freq * t * 2 * np.pi)
        yield note * 10000 #(32767 / np.max(np.abs(note))) * 0.1


def main():
    for note in note_gen():
        note = note.astype(np.int16)

        # start playback
        play_obj = sa.play_buffer(note, 1, 2, sample_rate)

        # wait for playback to finish before exiting
        play_obj.wait_done()

if __name__ == "__main__":
    main()
