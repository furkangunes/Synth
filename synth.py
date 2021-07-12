import threading
import numpy as np

from player import Player
from note import Note, NoteFactory
from gui import Gui

def main():
    freq = [0]
    keyboard = NoteFactory.create_keyboard(4)

    lock = threading.RLock()
    player_thread = threading.Thread(target=lambda: Player().play(freq, lock))
    player_thread.setDaemon(True)
    player_thread.start()

    gui = Gui(freq)
    gui.mainloop()

    player_thread.join()

if __name__ == "__main__":
    main()
