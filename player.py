import numpy as np
import pyaudio
from time import sleep

from modulators import Env, Osc

class Timer:
    def __init__(self, frame_rate):
        self.time = 0.0
        self.step_size = 1.0 / frame_rate

    def now(self):
        return self.time

    def tick(self):
        self.time += self.step_size

    def wind(self, amount):
        # Fast forward in case of no note being played
        self.time += amount * self.step_size

class Player(pyaudio.PyAudio):
    """
    Plays continously what is inside its buffer (with play method)
    """
    def __init__(self, *, frames_per_buffer=1024, frame_rate=44100, channels=1, format=pyaudio.paFloat32, output=True):
        pyaudio.PyAudio.__init__(self)
        self.buffer = np.zeros((frames_per_buffer, channels), dtype=np.float32)
        self.amplitude = 1.0

        self.notes = []

        self.timer = Timer(frame_rate)

        self.osc = Osc()
        self.osc.active_function = self.osc.sin_wave

        self.env = Env(step_size=self.timer.step_size, amplitude=0.5)

        self.frame_rate = frame_rate
        self.ostream = pyaudio.Stream(self, rate=frame_rate, frames_per_buffer=frames_per_buffer, channels=channels, format=format, output=output, stream_callback=self.callback)

        self.should_stop = False

    def callback(self, in_data, frame_count, time_info, status):
        if len(self.notes) == 0:
            self.buffer.fill(0.0)
            self.timer.wind(frame_count)
        else:
            #print(self.notes)
            for i in range(frame_count):
                output = 0.0

                # Traverse by index with while loop to be able to remove note while traversing
                j = 0
                while j < len(self.notes):
                    note = self.notes[j]

                    amp = self.env(note, self.timer.now(), self.amplitude)

                    if not note.is_active:
                        del self.notes[j]
                    else:
                        output += self.osc(note, self.timer.now(), amp)
                        j += 1

                self.buffer[i] = output
                self.timer.tick()

            i = 0
            while i < len(self.notes):
                if not self.notes[i].is_active:
                    del self.notes[i]
                else:
                    i += 1

        return self.buffer, pyaudio.paContinue

    def play(self):
        self.ostream.start_stream()

        while not self.should_stop and self.ostream.is_active():
            sleep(0.1)

        self.ostream.stop_stream()
        self.ostream.close()

# if __name__ == "__main__":
#     player = Player()
#     t = threading.Thread(target=player.play())
#     t.start()

#     #input()
#     player.should_stop = True
#     t.join()
#     player.terminate()