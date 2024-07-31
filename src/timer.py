"""
This timer runs in a separate thread and calls a callback function at each tick.
"""

import threading
import time


class CountdownTimer:
    """
    A countdown timer that runs in a separate thread and calls a callback function at each tick.
    """

    def __init__(self, hours, minutes, seconds, callback):
        """
        Initializes the CountdownTimer with the specified hours, minutes, and seconds.

        Args:
            hours (int): The number of hours for the countdown.
            minutes (int): The number of minutes for the countdown.
            seconds (int): The number of seconds for the countdown.
            callback (function): The function to call at each tick of the timer.
        """
        self.total_time = hours * 3600 + minutes * 60 + seconds
        self.callback = callback
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run)

    def start(self):
        """
        Starts the countdown timer in a separate thread.
        """
        self.thread.start()

    def _run(self):
        """
        Runs the countdown logic.
        """
        clock_time = self.total_time
        while clock_time > 0 and not self._stop_event.is_set():
            hours, remainder = divmod(clock_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.callback(hours, minutes, seconds, clock_time)
            time.sleep(1)
            clock_time -= 1

        if not self._stop_event.is_set():
            self.callback(0, 0, 0, 0, action=True)

    def stop(self):
        """
        Stops the countdown timer.
        """
        self._stop_event.set()
