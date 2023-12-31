import threading
import time


class Animation(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._event = threading.Event()

    def run(self):
        spin_chars = ["⣾ ", "⣽ ", "⣻ ", "⢿ ", "⡿ ", "⣟ ", "⣯ ", "⣷ "]
        i = 0
        while not self._event.is_set():
            print(f"\r{spin_chars[i]} Loading", end="")
            i = (i + 1) % len(spin_chars)
            time.sleep(0.08)

    def stop(self):
        self._event.set()
        self.join()
        print("\r" + " " * 10 + "\r", end="")  # Clear loading animation
