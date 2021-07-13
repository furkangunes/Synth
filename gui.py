import tkinter as tk

from note import Note, NoteFactory
from player import Player

class Gui(tk.Tk):
    def __init__(self, player: Player, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.player = player
        self.keyboard = NoteFactory.create_keyboard(key_count=15) # Might change key count
        self.key_dict = self.get_key_dict()

        self.set_bindings()

    def get_key_dict(self, octave_number=4):
        return {
            "a": "A" + str(octave_number),
            "w": "A" + str(octave_number) + "#",
            "s": "B" + str(octave_number),
            "d": "C" + str(octave_number + 1),
            "e": "C" + str(octave_number + 1) + "#",
            "f": "D" + str(octave_number + 1),
            "r": "D" + str(octave_number + 1) + "#",
            "g": "E" + str(octave_number + 1),
            "h": "F" + str(octave_number + 1),
            "y": "F" + str(octave_number + 1) + "#",
            "j": "G" + str(octave_number + 1),
            "u": "G" + str(octave_number + 1) + "#",
            "k": "A" + str(octave_number + 1),
            "o": "A" + str(octave_number + 2) + "#",
            "l": "B" + str(octave_number + 1),
        }

    def change_note(self, note_name):
        print("Active Note:", note_name, end="\r")
        self.player.freq = self.keyboard[note_name].freq

    def on_press(self, key):
        key_name = key.keysym

        if key_name in self.key_dict:
            self.change_note(self.key_dict[key_name])

    def on_release(self, key):
        print("No action" + " " * 6, end="\r")
        self.player.freq = 0

    def set_bindings(self, octave_number=4):
        self.bind("<Key>", self.on_press)
        self.bind("<KeyRelease>", self.on_release)