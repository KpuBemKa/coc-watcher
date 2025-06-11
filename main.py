import time
import sys
import argparse

from pynput.keyboard import Key, KeyCode, Listener

from modules.elixir_farm.builder_elixir_farmer import ElixirFarmer
from modules.battle_finder import BattleFinder
from settings import START_KEY, STOP_KEY, HARDSTOP_KEY


hardstop_flag = False

parser = argparse.ArgumentParser(
    prog="CoC flexer",
    description="Clash of Clans ultimate mega flexer",
    epilog="Text at the bottom of help",
)
parser.add_argument("-t", "--ths", help="Enumerate the desired TH levels to search via ',': --ths 11,12,13,...")


def verify_th_existence(th_id):
    return sys.


def main():
    try:
        args = parser.parse_args()
        ths_to_search = args.ths
        print(ths_to_search)
        # line_length = int(sys.argv[1])
        elixir_farmer = ElixirFarmer()
        battle_finder = BattleFinder()

        def key_press_listener(key: KeyCode | Key | None):
            if key == START_KEY:
                # elixir_farmer.start()
                battle_finder.start()
                print("Farmer started.")

            elif key == STOP_KEY:
                print("Stopping miner...")
                # elixir_farmer.stop()
                battle_finder.stop()
                print("Miner stopped.")

            elif key == HARDSTOP_KEY:
                print("Hardstopping...")
                global hardstop_flag
                hardstop_flag = True

        listener = Listener(on_press=key_press_listener)
        listener.start()

        print("Ready to farm elixir.")

        while True:
            if hardstop_flag:
                raise KeyboardInterrupt

            time.sleep(0.5)
    except ValueError:
        print("Error. Are you sure the first argument is an integer?")


main()
