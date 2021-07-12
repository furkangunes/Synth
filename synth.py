import tkinter as tk
import threading
import numpy as np

from player import Player
from note import Note, NoteFactory

def main():
    play_freq = [440]
    keyboard = NoteFactory.create_keyboard(4)

    lock = threading.RLock()
    player_thread = threading.Thread(target=lambda: Player().play(play_freq, lock))
    player_thread.setDaemon(True)
    player_thread.start()

    while True:
        print("Main:", play_freq)
        inp = input()

        #with lock:
        if inp == "b":
            play_freq = [keyboard[1].freq]
        elif inp == "c":
            play_freq = [keyboard[2].freq]

        else:
            play_freq = [1000]

        print("Got input")

    player_thread.join()

if __name__ == "__main__":
    main()
