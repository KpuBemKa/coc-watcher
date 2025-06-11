import threading
import os.path
import time

from screeninfo import get_monitors
from pynput.mouse import Button as MouseButton

from . import utils
from .pynput_singleton import MouseControllerSingleton, KeyboardControllerSingleton
from .datas import Position, Color, position_converter


class Coords:
    ATTACK_BUTTON = position_converter((2560, 1440), Position(140, 1295, 100, 100))
    FIND_MATCH_BUTTON = position_converter((2560, 1440), Position(1850, 860, 220, 90))
    NEXT_BATTLE_BUTTON = position_converter((2560, 1440), Position(2370, 1100, 170, 70))

    SEARCH_CLOUD = position_converter((2560, 1440), Position(2219, 643))


class Colors:
    SEARCH_CLOUD = Color(102, 79, 76)


class StopRequestedException(Exception):
    pass


class BattleFinder:
    def __init__(self, ths_to_search):
        self.__keyboard = KeyboardControllerSingleton()
        self.__mouse = MouseControllerSingleton()
        self.__ths = ths_to_search

        self.__started = False
        self.__stop_flag = False
        self.__worker_thread = threading.Thread(
            name="BattleFinderThread", target=self.__worker, daemon=True
        )

        # print(
        #     f"Cords:\n{Coords.ATTACK_BUTTON}\n{Coords.FIND_MATCH_BUTTON}\n{Coords.NEXT_BATTLE_BUTTON}\n{Coords.SEARCH_CLOUD}"
        # )

    def start(self):
        if self.__started:
            return

        self.__stop_flag = False
        self.__started = True
        self.__worker_thread.start()

    def stop(self):
        if not self.__started:
            return

        self.__stop_flag = True
        self.__worker_thread.join()
        self.__started = False

    def __worker(self):
        try:
            self.__start_battle()
            self.__wait_for_battle_start()
            self.__zoom_out()

            utils.move_mouse(Coords.NEXT_BATTLE_BUTTON)

            while True:
                if self.__is_enemy_th_in_range(self.__ths):
                    break

                print("TH is not in the given range. Skipping...")

                self.__click_next_battle()
                self.__wait_for_battle_start()

            print("-----\nA TH in the given range has been found. Quitting...\n(-----")
            self.__play_found_sound()

        except StopRequestedException:
            return

    def __is_enemy_th_in_range(self, th_range):
        for th_index in th_range:
            if self.__compare_enemy_th(th_index):
                return True
            print(f"This TH is not {th_index}")
            self.__sleep_with_check(0)

        return False

    def __compare_enemy_th(self, th_index):
        th_image_path = f"./static/ths/th-{th_index}.png"

        if not os.path.isfile(th_image_path):
            raise FileNotFoundError(f"{th_image_path} doesn't exist.")

        return utils.is_object_on_screen(th_image_path)

    def __start_battle(self):
        utils.click_with_randomization(Coords.ATTACK_BUTTON, MouseButton.left)
        self.__sleep_with_check(0.2)
        utils.click_with_randomization(Coords.FIND_MATCH_BUTTON, MouseButton.left)

    def __wait_for_battle_start(self):
        while True:
            time.sleep(1)

            if not Colors.SEARCH_CLOUD.is_similar(
                utils.get_color_in_position(Coords.SEARCH_CLOUD)
            ):
                break

        # self.__sleep_with_check(1)

    def __click_next_battle(self):
        utils.click_with_randomization(Coords.NEXT_BATTLE_BUTTON, MouseButton.left)

    def __zoom_out(self):
        monitor = get_monitors()[0]
        center_x = monitor.width // 2
        center_y = monitor.height // 2
        utils.move_mouse(Position(center_x, center_y))

        self.__sleep_with_check(0.1)

        for i in range(0, 5):
            self.__mouse.scroll(dx=0, dy=-10)
            self.__sleep_with_check(0.1)

    def __play_found_sound(self):
        pass

    def __sleep_with_check(
        self, sleep_time: float, max_delta: float | None = None
    ) -> None:
        """Sleeps the defined time, then checks if a stop has been requested

        Args:
            sleep_time (float): Amount of seconds to sleep

        Raises:
            StopRequestedException: If a stop has been requested (internal stop flag has been set)
        """
        if self.__stop_flag:
            raise StopRequestedException

        utils.random_sleep(sleep_time, max_delta)

        if self.__stop_flag:
            raise StopRequestedException
