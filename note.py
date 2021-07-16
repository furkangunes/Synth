from dataclasses import dataclass

from modulators import Env

@dataclass
class Note:
    name: str
    freq: float
    press_time = 0
    release_time = 0
    active = False

    @classmethod
    def from_name(cls: type, name: str):
        """
        Create a note from its name
        E.g. note.from_class("C4#")
        """

        A_freq = 55 * 2 ** ((int(name[1]) - 1))
        power = (ord(name[0]) - 65) * 2 / 12

        if len(name) == 3:
            if name[2] == "#":
                power += 1 / 12
            else:
                power -= 1 / 12

        freq = A_freq * 2 ** power

        return cls(name, freq, None, None)

class NoteFactory:
    @staticmethod
    def create_keyboard(octave_number=4, key_count=20) -> dict:
        """
        Creates 20 notes including sharps
        E.g. A4, A4#, B4, C4, C4#, ..., E6
        """

        keyboard = {}
        freq = 55 * 2 ** (octave_number - 1)
        letter = 'A'
        name = letter + str(octave_number)

        for i in range(key_count):
            keyboard[name] = Note(name, freq)

            if i % 12 in (0, 3, 5, 8, 10):
                name = letter + str(octave_number) + '#'
            else:
                letter = chr(ord(letter) + 1)
                if letter == 'C':
                    octave_number += 1
                elif letter > 'G':
                    letter = 'A'

                name = letter + str(octave_number)

            freq *= 2 ** (1 / 12)

        return keyboard