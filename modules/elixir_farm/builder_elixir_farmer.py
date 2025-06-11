import threading

from screeninfo import get_monitors
from pynput.keyboard import Key
from pynput.mouse import Button as MouseButton

from modules.pynput_singleton import MouseControllerSingleton, KeyboardControllerSingleton
from modules.datas import Position
from modules import utils

from .defines import Coords, Colors
from .elixir_battle_executor import ElixirBattleExecutor


class StopRequestedException(Exception):
    pass


class ElixirCartNotFoundException(Exception):
    pass


class ElixirFarmer:
    def __init__(self):
        self.__keyboard = KeyboardControllerSingleton()
        self.__mouse = MouseControllerSingleton()

        self.__started = False
        self.__stop_flag = False
        self.__worker_thread = threading.Thread(
            name="ElixirFarmerThread", target=self.__worker, daemon=True
        )

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
            self.__align_village()
            # self.__sleep_with_check(0.5)

            self.__enter_cart()
            self.__sleep_with_check(1, max_delta=0.5)

            while True:
                finished_battles = self.__count_finished_battles()
                print(f"Finished battles: {finished_battles}")
                if finished_battles > 0:
                    self.__claim_cart_elixir()
                    self.__sleep_with_check(0.5)

                in_progress_battles = self.__count_in_progress_battles()
                print(f"Battles in progress: {in_progress_battles}")
                if in_progress_battles < 4:
                    utils.press_key_with_randomization(Key.esc)

                    for _ in range(4 - in_progress_battles):
                        ElixirBattleExecutor().execute_battle()
                        self.__sleep_with_check(0.5)

                    self.__align_village()
                    self.__enter_cart()
                    self.__sleep_with_check(1, max_delta=0.5)

        except StopRequestedException:
            return

        except ElixirCartNotFoundException:
            print("Elixir Card was not found. Terminating...")
            return

    def __enter_cart(self):
        position = utils.find_object_on_screen(
            "F:/dev/projects/coc_watcher/static/elixir-cart-cropped.png"
        )

        if position is None:
            raise ElixirCartNotFoundException

        print(f"Card position: {position.x}, {position.y}")

        utils.click_with_randomization(position, MouseButton.left)

    def __count_finished_battles(self) -> int:
        count = 0

        for icon_pos in Coords.ELIXIR_ICONS:
            if Colors.ELIXIR_ICON.is_similar(utils.get_color_in_position(icon_pos)):
                count += 1

        return count

    def __count_in_progress_battles(self) -> int:
        count = 0

        for icon_pos in Coords.BATTLE_ROWS:
            if Colors.BATTLE_ROW_IN_PROGRESS.is_similar(
                utils.get_color_in_position(icon_pos)
            ):
                count += 1

        return count

    def __align_village(self) -> None:
        monitor = get_monitors()[0]
        center_x = monitor.width // 2
        center_y = monitor.height // 2
        utils.move_mouse(Position(center_x, center_y))

        self.__sleep_with_check(0.1)

        for i in range(0, 5):
            self.__mouse.scroll(dx=0, dy=-10)
            self.__sleep_with_check(0.1)

        self.__mouse.press(MouseButton.left)
        self.__sleep_with_check(0.1)
        utils.move_mouse(Position(center_x, center_y + 400))
        self.__sleep_with_check(0.1)
        self.__mouse.release(MouseButton.left)

    def __claim_cart_elixir(self):
        utils.click_with_randomization(Coords.COLLECT_BUTTON, MouseButton.left)

    def __sleep_with_check(
        self, sleep_time: float, max_delta: float | None = None
    ) -> None:
        """Sleeps the defined time, then checks if a stop has been requested

        Args:
            sleep_time (float): Amount of seconds to sleep

        Raises:
            StopRequestedException: If a stop has been requested (internal stop flag has been set)
        """
        utils.random_sleep(sleep_time, max_delta)

        if self.__stop_flag:
            raise StopRequestedException
