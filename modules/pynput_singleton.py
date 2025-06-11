from threading import Lock
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController


class MouseControllerSingleton:
    _instance = None
    _lock = Lock()  # For thread-safety in multi-threaded environments

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                # Only create the instance if it doesn't already exist
                cls._instance = super().__new__(cls)
                cls._instance.controller = MouseController()
        return cls._instance.controller  # Return the controller directly


class KeyboardControllerSingleton:
    _instance = None
    _lock = Lock()  # For thread-safety in multi-threaded environments

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                # Only create the instance if it doesn't already exist
                cls._instance = super().__new__(cls)
                cls._instance.controller = KeyboardController()
        return cls._instance.controller  # Return the controller directly
