import os
import time
import argparse

from pynput.keyboard import Key, KeyCode, Listener

from modules.battle_finder import BattleFinder
from settings import START_KEY, STOP_KEY, HARDSTOP_KEY


hardstop_flag = False

parser = argparse.ArgumentParser(
    prog="CoC flexer",
    description="Clash of Clans ultimate mega flexer",
    epilog="Text at the bottom of help",
)
parser.add_argument(
    "-t",
    "--ths",
    help="Enumerate the desired TH levels to search via ',': --ths 11,12,13,...",
)


def verify_th_existence(th_id):
    return os.path.isfile(f"./static/ths/th-{th_id}.png")


def main():
    try:
        args = parser.parse_args()
        ths_to_search: str = args.ths
        th_indexes = ths_to_search.split(",")

        for th_index in th_indexes:
            if not verify_th_existence(th_index):
                print(
                    f"Unknown TH level encountered: {th_index}. Please try something else."
                )

        battle_finder = BattleFinder(th_indexes)

        def key_press_listener(key: KeyCode | Key | None):
            if key == START_KEY:
                battle_finder.start()
                print("Battle searcher started. Press F7 to stop")

            elif key == STOP_KEY:
                print("Stopping battle searcher...")
                battle_finder.stop()
                print("Battle searcher stopped.")

            elif key == HARDSTOP_KEY:
                print("Hardstopping...")
                global hardstop_flag
                hardstop_flag = True

        listener = Listener(on_press=key_press_listener)
        listener.start()

        print(f"Searching for the next THs: {'; '.join(th_indexes)};")
        print("Ready to search for a battle. Enter the game, and press F6 to start.")

        while True:
            if hardstop_flag:
                raise KeyboardInterrupt

            time.sleep(0.5)
    except ValueError:
        print("Error. Are you sure the arguments are OK?")


main()
