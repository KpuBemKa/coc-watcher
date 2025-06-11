import time

from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button as MouseButton
from pynput.mouse import Controller as MouseController

from modules import utils

from .defines import Coords, Colors, Position


class ElixirBattleExecutor:
    def __init__(self):
        self.__keyboard: KeyboardController = KeyboardController()
        self.__mouse = MouseController()

    def execute_battle(self):
        self.__start_battle()
        self.__wait_for_battle_start()

        print("Battle started.")

        self.__place_unit("q", Coords.UNIT_PLACEMENT)
        utils.random_sleep(0.2)
        self.__end_battle()

    def __start_battle(self):
        utils.click_with_randomization(Coords.ATTACK_BUTTON, MouseButton.left)
        utils.random_sleep(0.2)
        utils.click_with_randomization(Coords.FIND_ATTACK_BUTTON, MouseButton.left)

    def __wait_for_battle_start(self):
        while True:
            time.sleep(1)

            if not Colors.BATTLE_SEARCHING.is_similar(
                utils.get_color_in_position(Coords.BATTLE_WAIT)
            ):
                break

        utils.random_sleep(3)

    def __place_unit(self, unit_key: Key, position: Position) -> None:
        self.__keyboard.press(unit_key)
        utils.random_sleep(0.1)
        self.__keyboard.release(unit_key)
        utils.random_sleep(0.2)

        utils.click_with_randomization(position, MouseButton.left)

    def __end_battle(self):
        self.__keyboard.press(Key.esc)
        utils.random_sleep(0.1)
        self.__keyboard.release(Key.esc)
        utils.random_sleep(0.2)

        utils.click_with_randomization(Coords.END_OKAY_BUTTON, MouseButton.left)

        self.__keyboard.press(Key.esc)
        utils.random_sleep(0.1)
        self.__keyboard.release(Key.esc)
        utils.random_sleep(0.2)
