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
        self.amplitude = 0.6

        self.notes = []

        self.timer = Timer(frame_rate)

        self.env = Env(amplitude=self.amplitude)
        self.osc = Osc()
        #self.osc.active_function = self.osc.sin_wave

        self.frame_rate = frame_rate
        self.ostream = pyaudio.Stream(self, rate=frame_rate, frames_per_buffer=frames_per_buffer, channels=channels, format=format, output=output, stream_callback=self.callback)

        self.should_stop = False

    def change_wave_form(self, wave_form_name):
        self.osc.change_active_func(wave_form_name)
    
    def toggle_vibrato(self):
        # Returns its state
        self.osc.vibrato.is_active = not self.osc.vibrato.is_active
        return self.osc.vibrato.is_active

    def toggle_noise(self):
        # Returns its state
        self.osc.noise_enabled = not self.osc.noise_enabled
        return self.osc.noise_enabled

    # TODO: Does not work with Stereo currently
    def callback(self, in_data, frame_count, time_info, status):
        if len(self.notes) == 0:
            self.buffer.fill(0.0)
            self.timer.wind(frame_count)
        else:
            for i in range(frame_count):
                output = 0.0

                # Traverse by index with while loop to be able to remove note while traversing
                j = 0
                amps = []
                while j < len(self.notes):
                    note = self.notes[j]

                    amp = self.env(note, self.timer.now(), self.amplitude)
                    if not note.is_active:
                        del self.notes[j]
                    else:
                        amps.append(amp)
                        j += 1

                amps = [amp / len(amps) for amp in amps]

                for note in self.notes:
                    output += self.osc(note.freq, self.timer.now(), amps[self.notes.index(note)])

                self.buffer[i] = output
                self.timer.tick()

        return self.buffer, pyaudio.paContinue

    def play(self):
        self.ostream.start_stream()

        while not self.should_stop and self.ostream.is_active():
            sleep(0.1)

        self.ostream.stop_stream()
        self.ostream.close()
