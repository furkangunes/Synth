import tkinter as tk
from tkinter import messagebox

from note import Note, NoteFactory
from player import Player

class Frame(tk.Frame):
    def __init__(self, master=None, cnf={}, **kwargs):
        tk.Frame.__init__(master=master, cnf=cnf, **kwargs)

GIT_LINK = "https://github.com/furkangunes/Synth"
MAIN_NOTE_COLOR = "orange"
SHARP_NOTE_COLOR = "black"

class Gui(tk.Tk):
    def __init__(self, player: Player, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.player = player
        self.octave_number = 3
        self.keyboard = NoteFactory.create_keyboard(octave_number=self.octave_number, key_count=20) # Might change key count
        self.key_dict = self.get_key_dict()
        self.button_dict = dict.fromkeys(self.key_dict.keys())

        self.header = tk.Frame(master=self, width=200, height=100)
        self.keyboard_frame = tk.Frame(master=self, width=200, height=100)
        self.footer = tk.Frame(master=self, width=200, height=100, bg="blue")

        self.detail = "Press keys to play sound"
        self.detail_label: tk.Label

        self.configure_frames()
        self.configure_keyboard_frame()

        self.set_bindings()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.resizable(False, False)

    def configure_frames(self):
        self.title("Synthesizer")

        self.header.grid(row=0)
        self.keyboard_frame.grid(row=1)
        self.footer.grid(row=2)

        self.update()

        tk.Label(master=self.header, text="Synthesizer", bg="red").grid(row=0, sticky="NSEW")
        self.detail_label = tk.Label(master=self.header, text=self.detail)
        self.detail_label.grid(row=1, sticky="NSEW")

        tk.Label(master=self.footer, text=GIT_LINK, bg="red").grid(row=0)

    def configure_keyboard_frame(self):
        button_width: int

        for i, key in zip(range(12), "asdfghjklşi,"):
            note_name = self.key_dict[key] + "\n" * 5 + key.upper()
            button = tk.Button(
                master=self.keyboard_frame,
                width=10,
                height=20,
                text=note_name,
                anchor="s",
                foreground=SHARP_NOTE_COLOR,
                bg=MAIN_NOTE_COLOR,
                highlightthickness=True
            )
            button.grid(row=0, column=i)

            self.button_dict[key] = {"button": button, "color": MAIN_NOTE_COLOR}

        self.update()    
        button_width = button.winfo_width()

        sharp_buttons = []
        for key in "weryuıpğ":
            button = tk.Button(
                master=self.keyboard_frame,
                width=5,
                height=10,
                text=self.key_dict[key] + "\n" * 5 + key.upper(),
                anchor="s",
                foreground="white",
                bg=SHARP_NOTE_COLOR,
                highlightthickness=True
            )

            sharp_buttons.append(button)
            self.button_dict[key] = {"button": button, "color": SHARP_NOTE_COLOR}

        # Below is hard coded :(
        sharp_buttons[0].place(x=button_width - 25)
        sharp_buttons[1].place(x=button_width * 3 - 25)
        sharp_buttons[2].place(x=button_width * 4 - 25)
        sharp_buttons[3].place(x=button_width * 6 - 25)
        sharp_buttons[4].place(x=button_width * 7 - 25)
        sharp_buttons[5].place(x=button_width * 8 - 25)
        sharp_buttons[6].place(x=button_width * 10 - 25)
        sharp_buttons[7].place(x=button_width * 11 - 25)

    def get_key_dict(self):
        return {
            "a": "A" + str(self.octave_number),
            "w": "A" + str(self.octave_number) + "#",
            "s": "B" + str(self.octave_number),
            "d": "C" + str(self.octave_number + 1),
            "e": "C" + str(self.octave_number + 1) + "#",
            "f": "D" + str(self.octave_number + 1),
            "r": "D" + str(self.octave_number + 1) + "#",
            "g": "E" + str(self.octave_number + 1),
            "h": "F" + str(self.octave_number + 1),
            "y": "F" + str(self.octave_number + 1) + "#",
            "j": "G" + str(self.octave_number + 1),
            "u": "G" + str(self.octave_number + 1) + "#",
            "k": "A" + str(self.octave_number + 1),
            "ı": "A" + str(self.octave_number + 1) + "#",
            "l": "B" + str(self.octave_number + 1),
            "ş": "C" + str(self.octave_number + 2),
            "p": "C" + str(self.octave_number + 2) + "#",
            "i": "D" + str(self.octave_number + 2),
            "ğ": "D" + str(self.octave_number + 2) + "#",
            ",": "E" + str(self.octave_number + 2)
        }

    def activate_note(self, note_name):
        self.player.freq = self.keyboard[note_name].freq
        self.detail_label.config(text=f"{self.player.freq:.2f}" + " Hz")

    def on_press(self, key):
        key_name = key.char.lower()

        # Tk gets special chars at press but on release, so save duplicate of special char with keycode
        if key.keysym == "??":
            self.key_dict[key.keycode] = self.key_dict[key_name]
            self.button_dict[key.keycode] = self.button_dict[key_name]

        if key_name in self.key_dict:
            self.button_dict[key_name]["button"]["bg"] = "red"
            self.activate_note(self.key_dict[key_name])

    def on_release(self, key):
        self.detail_label.config(text="0.0 Hz")

        if key.keysym == "??":
            key_name = key.keycode
        else:
            key_name = key.char.lower()

        if key_name in self.button_dict:
            button, color = self.button_dict[key_name].values()
            button["bg"] = color

        self.player.freq = 0

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.player.should_stop = True
            self.destroy()

    def set_bindings(self, octave_number=4):
        self.bind("<Key>", self.on_press)
        self.bind("<KeyRelease>", self.on_release)