import tkinter as tk
from tkinter import messagebox

from note import Note, NoteFactory
from player import Player

class Frame(tk.Frame):
    def __init__(self, master=None, cnf={}, **kwargs):
        tk.Frame.__init__(master=master, cnf=cnf, **kwargs)

GIT_LINK = "https://github.com/furkangunes/Synth"

class Gui(tk.Tk):
    def __init__(self, player: Player, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.player = player
        self.keyboard = NoteFactory.create_keyboard(key_count=20) # Might change key count
        self.key_dict = self.get_key_dict()

        self.explanation = "Press keys to play sound"

        self.header = tk.Frame(master=self, width=200, height=100)
        self.keyboard_frame = tk.Frame(master=self, width=200, height=100, bg="green")
        self.footer = tk.Frame(master=self, width=200, height=100, bg="blue")

        self.configure_frames()
        self.configure_keyboard_frame()

        self.set_bindings()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        #self.header = tk.Frame(self, row=0, column=0, sticky="NSWE")

        print("No action" + " " * 7, end="\r")

    def configure_frames(self):
        self.title("Synthesizer")

        self.header.grid(row=0)
        self.keyboard_frame.grid(row=1)
        self.footer.grid(row=2)

        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

        tk.Label(master=self.header, text="Synthesizer", bg="red").grid(row=0)
        tk.Label(master=self.header, text=self.explanation).grid(row=1)

        tk.Label(master=self.footer, text=GIT_LINK, bg="red").grid(row=0)

    def configure_keyboard_frame(self):
        for i in range(8):
            tk.Frame(master=self.keyboard_frame, width=50, height=100, bg="orange", highlightthickness=1).grid(row=0, column=i)

        for i in range(12):
            tk.Frame(master=self.keyboard_frame, width=50, height=100, bg="orange", highlightthickness=1).grid(row=1, column=i)

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
            "ı": "A" + str(octave_number + 1) + "#",
            "l": "B" + str(octave_number + 1),
            "ş": "C" + str(octave_number + 2),
            "p": "C" + str(octave_number + 2) + "#",
            "i": "D" + str(octave_number + 2),
            "ğ": "D" + str(octave_number + 2) + "#",
            ",": "E" + str(octave_number + 2)
        }

    def change_note(self, note_name):
        print("Active Note:", note_name, end="\r")
        self.player.freq = self.keyboard[note_name].freq

    def on_press(self, key):
        key_name = key.char

        if key_name in self.key_dict:
            self.change_note(self.key_dict[key_name])

    def on_release(self, key):
        print("No action" + " " * 7, end="\r")
        self.player.freq = 0

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.player.should_stop = True
            self.destroy()

    def set_bindings(self, octave_number=4):
        self.bind("<Key>", self.on_press)
        self.bind("<KeyRelease>", self.on_release)