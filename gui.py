import tkinter as tk
from tkinter import messagebox
from os.path import join as path_join
from math import inf

from note import Note, NoteFactory
from player import Player

GIT_LINK = "https://github.com/furkangunes/Synth"

BACKGROUND_COLOR = "white"

MAIN_NOTE_COLOR = "orange"
SHARP_NOTE_COLOR = "black"

BUTTON_ENABLED_COLOR = "white"
BUTTON_DISABLED_COLOR = "grey"

HELP_TEXT = """
Play sound by pressing on your keyboards denoted on the keys in your screen.

You can select a different wave form by clicking the buttons on the right, each of which represented by their wave form symbols.

Vibrato makes the sound a little vibrating to get a different sound experience

Noise can be used to get a different type of instrumental sound, might be good with square wave.

You can slide the keyboard to left or right by pressing to the arrows below.

Shortcuts:
    Left Arrow: Shift keyboard to left
    Right Arrow: Shift keyboard to right
        
    Ctrl+v: Toggle Vibrato
    Ctrl+n: Toggle Noise
"""

class Gui(tk.Tk):
    def __init__(self, player: Player, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.config(bg=BACKGROUND_COLOR)

        self.player = player
        self.octave_number = 4
        self.keyboard = NoteFactory.create_keyboard(octave_number=self.octave_number, key_count=20) # Might change key count
        self.key_dict = self.get_key_dict()
        self.button_dict = dict.fromkeys(self.key_dict.keys())

        self.header = tk.Frame(master=self)
        self.keyboard_frame = tk.Frame(master=self)
        self.footer = tk.Frame(master=self, bg=BACKGROUND_COLOR)
        self.options_frame = tk.Frame(master=self, bg=BACKGROUND_COLOR)

        self.wave_buttons = {}
        
        self.vibrato_toggle: tk.Button
        self.noise_toggle: tk.Button
        self.octave_shift_left_button: tk.Button
        self.octave_shift_right_button: tk.Button

        self.active_wave_form = "sin"

        try:
            self.icons = {
                "sin": tk.PhotoImage(file=path_join("icons", "sin_wave_icon.png")).subsample(3, 3),
                "sqr": tk.PhotoImage(file=path_join("icons", "square_wave_icon.png")).subsample(3, 3),
                "tri": tk.PhotoImage(file=path_join("icons", "triangle_wave_icon.png")).subsample(3, 3),
                "saw": tk.PhotoImage(file=path_join("icons", "sawtooth_wave_icon.png")).subsample(3, 3),
                "on_toggle": tk.PhotoImage(file=path_join("icons", "on_toggle_icon.png")),
                "off_toggle": tk.PhotoImage(file=path_join("icons", "off_toggle_icon.png")),
                "left_arrow": tk.PhotoImage(file=path_join("icons", "left_arrow_icon.png")),
                "right_arrow": tk.PhotoImage(file=path_join("icons", "right_arrow_icon.png")),
                "help": tk.PhotoImage(file=path_join("icons", "help_icon.png"))
            }
        except Exception:
            self.player.should_stop = True

        self.detail = "Press keys to play sound"
        self.detail_label: tk.Label

        self.configure_frames()
        self.configure_keyboard_frame()

        self.set_bindings()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.resizable(False, False)

    def shift_keyboard(self, to_left):
        if (self.octave_number < 1 and to_left) or (self.octave_number > 6 and not to_left):
            return

        self.octave_number = self.octave_number - 1 if to_left else self.octave_number + 1
        self.keyboard = NoteFactory.create_keyboard(octave_number=self.octave_number, key_count=20)
        self.key_dict = self.get_key_dict()
        
        for key, button_tuple in zip(self.key_dict.keys(), self.button_dict.values()):
            button_tuple["button"].config(text=self.key_dict[key] + "\n" * 5 + key.upper())

    def configure_frames(self):
        self.title("Synthesizer")

        self.header.grid(row=0)
        self.keyboard_frame.grid(row=1)
        self.footer.grid(row=2)

        self.update()

        tk.Label(master=self.header, text="Synthesizer", bg="red").grid(row=0, sticky="NSEW")

        self.detail_label = tk.Label(master=self.header, text=self.detail)
        self.detail_label.grid(row=1, sticky="NSEW")

        self.octave_shift_left_button = tk.Button(
            master=self.footer,
            image=self.icons["left_arrow"],
            command=lambda: self.shift_keyboard(to_left=True)
        )

        self.octave_shift_right_button = tk.Button(
            master=self.footer,
            image=self.icons["right_arrow"],
            command=lambda: self.shift_keyboard(to_left=False)
        )

        self.octave_shift_left_button.grid(row=0, column=0)
        self.octave_shift_right_button.grid(row=0, column=1)

        tk.Label(master=self.footer, text=GIT_LINK, bg="red").grid(row=1)

        self.options_frame.grid(row=1, column=1)
        self.configure_options_frame()

    def configure_options_frame(self):
        # Wave form selection buttons
        self.wave_buttons["sin"] = tk.Button(
            master=self.options_frame,
            image=self.icons["sin"],
            command=lambda: self.change_wave_form("sin"),
            state=tk.DISABLED, # Initial wave form
            bg=BUTTON_DISABLED_COLOR # Initial wave form
        )

        self.wave_buttons["sqr"] = tk.Button(
            master=self.options_frame,
            image=self.icons["sqr"],
            command=lambda: self.change_wave_form("sqr"),
            state=tk.NORMAL,
            bg=BUTTON_ENABLED_COLOR
        )

        self.wave_buttons["tri"] = tk.Button(
            master=self.options_frame,
            image=self.icons["tri"],
            command=lambda: self.change_wave_form("tri"),
            state=tk.NORMAL,
            bg=BUTTON_ENABLED_COLOR
        )

        self.wave_buttons["saw"] =  tk.Button(
            master=self.options_frame,
            image=self.icons["saw"],
            command=lambda: self.change_wave_form("saw"),
            state=tk.NORMAL,
            bg=BUTTON_ENABLED_COLOR
        )

        # Help button
        tk.Button(
            master=self.options_frame,
            image=self.icons["help"],
            command=lambda: messagebox.showinfo(title="Help", message=HELP_TEXT)
        ).grid(row=0, column=1)

        # Dummy frame for padding in grid
        tk.Frame(master=self.options_frame, height=20).grid(row=1)

        tk.Label(master=self.options_frame, text="Vibrato", bg=BACKGROUND_COLOR).grid(row=2, column=0)

        self.vibrato_toggle = tk.Button(
            master=self.options_frame,
            image=self.icons["off_toggle"],
            command=self.toggle_vibrato,
            relief=tk.SUNKEN,
            highlightthickness=0,
            bd=0
        )

        tk.Label(master=self.options_frame, text="Noise", bg=BACKGROUND_COLOR).grid(row=3, column=0)

        self.noise_toggle = tk.Button(
            master=self.options_frame,
            image=self.icons["off_toggle"],
            command=self.toggle_noise,
            relief=tk.SUNKEN,
            highlightthickness=0,
            bd=0
        )

        self.vibrato_toggle.grid(row=2, column=1)
        self.noise_toggle.grid(row=3, column=1)

        # Dummy frame for padding in grid
        tk.Frame(master=self.options_frame, height=20).grid(row=4)

        self.wave_buttons["sin"].grid(row=5, column=0)
        self.wave_buttons["sqr"].grid(row=5, column=1)
        self.wave_buttons["tri"].grid(row=6, column=0)
        self.wave_buttons["saw"].grid(row=6, column=1)


        self.update()

    def configure_keyboard_frame(self):
        button_width: int

        for i, key in zip(range(12), "asdfghjkl??i,"):
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
        for key in "weryu??p??":
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
            "??": "A" + str(self.octave_number + 1) + "#",
            "l": "B" + str(self.octave_number + 1),
            "??": "C" + str(self.octave_number + 2),
            "p": "C" + str(self.octave_number + 2) + "#",
            "i": "D" + str(self.octave_number + 2),
            "??": "D" + str(self.octave_number + 2) + "#",
            ",": "E" + str(self.octave_number + 2)
        }

    def activate_note(self, note_name):
        note = self.keyboard[note_name]
        if note not in self.player.notes or note.is_active is False:
            note.press_time = self.player.timer.now()
            note.release_time = inf
            note.is_active = True
            self.player.notes.append(self.keyboard[note_name])

    def deactivate_note(self, note_name):
        note = self.keyboard[note_name]

        if note in self.player.notes: # Extra guard
            note.release_time = self.player.timer.now()
            #note.is_active = False

    def on_press(self, key):
        # TODO: It keeps activating note on key hold or, activate note appends and envelope removes immediately
        key_name = key.char.lower()

        # Tk gets special chars at press but on release, so save duplicate of special char with keycode
        # Ignore exceptions on press "FN" key or such
        try:
            if key.keysym == "??":
                self.key_dict[key.keycode] = self.key_dict[key_name]
                self.button_dict[key.keycode] = self.button_dict[key_name]
        except Exception:
            pass

        if key_name in self.key_dict:
            self.button_dict[key_name]["button"]["bg"] = "red"
            self.activate_note(self.key_dict[key_name])

    def on_release(self, key):
        if key.keysym == "??":
            key_name = key.keycode
        else:
            key_name = key.char.lower()

        if key_name in self.button_dict:
            button, color = self.button_dict[key_name].values()
            button["bg"] = color

            self.deactivate_note(self.key_dict[key_name])

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.player.should_stop = True
            self.destroy()

    def change_wave_form(self, wave_form_name):
        # Enable old button form back
        active_button = self.wave_buttons[self.active_wave_form]
        active_button["state"] = tk.NORMAL
        active_button["bg"] = BUTTON_ENABLED_COLOR

        # Choose and disabled new button form
        self.active_wave_form = wave_form_name
        active_button = self.wave_buttons[self.active_wave_form]
        active_button["state"] = tk.DISABLED
        active_button["bg"] = BUTTON_DISABLED_COLOR
        
        # Change wave form on player
        self.player.change_wave_form(self.active_wave_form)

    def toggle_vibrato(self):
        self.vibrato_toggle.config(image=self.icons["on_toggle" if self.player.toggle_vibrato() else "off_toggle"])

    def toggle_noise(self):
        self.noise_toggle.config(image=self.icons["on_toggle" if self.player.toggle_noise() else "off_toggle"])

    def set_bindings(self, octave_number=4):
        self.bind("<Key-Left>", lambda _: self.shift_keyboard(to_left=True))
        self.bind("<Key-Right>", lambda _: self.shift_keyboard(to_left=False))

        self.bind("<Control-v>", lambda _: self.toggle_vibrato())
        self.bind("<Control-V>", lambda _: self.toggle_vibrato())

        self.bind("<Control-n>", lambda _: self.toggle_noise())
        self.bind("<Control-N>", lambda _: self.toggle_noise())

        self.bind("<Key>", self.on_press)
        self.bind("<KeyRelease>", self.on_release)
