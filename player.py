import numpy as np
import pyaudio
#from threading import RLock
import threading
from time import sleep

class Osc():
    """
    An oscillator to get more interesting sin waves
    """

    def __init__(self):
        self.active_function: self.sin_wave

    def sin_wave(self, phase, amplitude):
        # Return original sin wave
        return amplitude * np.sin(phase)

    def sqr_wave(self, phase, amplitude):
        # Return square shaped sin wave, which only alters between -1 and 1
        return np.sign(self.sin_wave(phase, amplitude))

    def tri_wave(self, phase, amplitude):
        # Return triangular shaped sin wave, which forms a triangle over sin wave by its peak values
        return 2.0 * amplitude / np.pi * np.arcsin(self.sin_wave(phase, amplitude))

    def saw_wave(self, phase, amplitude):
        # Returns a saw tooth shaped cummulatively sampled sin waves
        f = 440.0
        t = phase / (2.0 * np.pi * f)

        return 2.0 * amplitude / np.pi * (f * np.pi * (t % (1.0 / f)) - np.pi / 2.0)

    def __call__(self, phase, amplitude):
        # Call object directly with phase and amplitude (osc = Osc(); osc(phase, amplitude))
        return self.active_function(phase, amplitude)

class Player(pyaudio.PyAudio):
    """
    Plays continously what is inside its buffer (with play method)
    """
    def __init__(self, *, frames_per_buffer=1024, frame_rate=44100, channels=1, format=pyaudio.paFloat32, output=True):
        pyaudio.PyAudio.__init__(self)
        self.buffer = np.zeros((frames_per_buffer, channels), dtype=np.float32)
        self.amplitude = 1.0
        self.phase = 0
        self.freq = 0.0
        self.osc = Osc()
        self.osc.active_function = self.osc.saw_wave

        self.frame_rate = frame_rate
        self.ostream = pyaudio.Stream(self, rate=frame_rate, frames_per_buffer=frames_per_buffer, channels=channels, format=format, output=output, stream_callback=self.callback)

        self.should_stop = False

    def callback(self, in_data, frame_count, time_info, status):
        for i in range(frame_count):
            self.phase += 2 * np.pi * self.freq / self.frame_rate
            self.buffer[i] = self.osc(self.phase, self.amplitude)

        return (self.buffer, pyaudio.paContinue)

    def play(self):
        self.ostream.start_stream()

        while not self.should_stop and self.ostream.is_active():
            sleep(0.1)

        self.ostream.stop_stream()
        self.ostream.close()

if __name__ == "__main__":
    player = Player()
    t = threading.Thread(target=player.play())
    t.start()

    #input()
    player.should_stop = True
    t.join()
    player.terminate()