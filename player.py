import numpy as np
import pyaudio
#from threading import RLock
import threading
from time import sleep

# TODO: Try to generalize magic numbers

class Player(pyaudio.PyAudio):
    def __init__(self, *, frames_per_buffer=1024, frame_rate=44100, channels=1, format=pyaudio.paInt32, output=True):
        pyaudio.PyAudio.__init__(self)
        self.buffer = np.empty((frames_per_buffer, channels))
        self.phase = 0
        self.freq = 440.0
        self.frame_rate = frame_rate
        self.ostream = pyaudio.Stream(self, rate=frame_rate, frames_per_buffer=frames_per_buffer, channels=channels, format=format, output=output, stream_callback=self.callback)

        self.should_stop = False

    def callback(self, in_data, frame_count, time_info, status):
        # TODO: Adjust according to channels
        for i in range(frame_count):
            self.buffer[i] = int(32767 * 0.5 * np.sin(self.phase))
            self.phase += 2 * np.pi * self.freq / self.frame_rate

        return (self.buffer, pyaudio.paContinue)

    def play(self):
        self.ostream.start_stream()

        while self.ostream.is_active() and not self.should_stop:
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