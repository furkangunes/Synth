import numpy as np
import pyaudio
#from threading import RLock
import threading
from time import sleep

from modulators import Env, Osc

class Player(pyaudio.PyAudio):
    """
    Plays continously what is inside its buffer (with play method)
    """
    def __init__(self, *, frames_per_buffer=1024, frame_rate=44100, channels=1, format=pyaudio.paFloat32, output=True):
        pyaudio.PyAudio.__init__(self)
        self.buffer = np.zeros((frames_per_buffer, channels), dtype=np.float32)
        self.amplitude = 1.0
        self.phase = 0
        self.notes = []

        self.osc = Osc()
        self.osc.active_function = self.osc.sin_wave

        self.env = Env(sustain_amplitude=0.5)

        self.frame_rate = frame_rate
        self.ostream = pyaudio.Stream(self, rate=frame_rate, frames_per_buffer=frames_per_buffer, channels=channels, format=format, output=output, stream_callback=self.callback)

        self.should_stop = False
        self.t = 0

    def callback(self, in_data, frame_count, time_info, status):
        if len(self.notes) == 0:
            self.buffer.fill(0.0)
        else:
            for i in range(frame_count):
                # TODO: Change freq to notes' total calculated freq
                self.phase += 2 * np.pi * self.freq / self.frame_rate
                self.buffer[i] = self.osc(self.phase, self.amplitude, self.freq)

                #self.buffer[i] = self.amplitude * np.sin(2 * np.pi * self.t * self.freq / self.frame_rate)
                #self.t += 1

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