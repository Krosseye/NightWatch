"""
NightWatch helps create a sleep-friendly environment by managing your devices during bedtime.

This script sets up the UI and handles the countdown timer.
"""

import logging
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

import sv_ttk
from actions import pause_media, shutdown_system, sleep_system

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def resource_path(relative_path):
    """Get absolute path to resource (works for dev and bin)"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        base_path = os.path.join(current_dir, "resources")
    return os.path.join(base_path, relative_path)


class NightWatch(tk.Tk):
    """
    Main application class (subclass of tk.Tk)

    This class initializes and sets up the main application window and its components.
    """

    def __init__(self):
        super().__init__()
        self.setup_window()

        self.lbf_action = ttk.LabelFrame(self, text="Select Action", padding=5)
        action_options = ["Pause", "Sleep", "Shutdown"]

        self.cmb_actions = ttk.Combobox(
            self.lbf_action, values=action_options, state="readonly"
        )
        self.hour_string = tk.StringVar(value="00")
        self.minute_string = tk.StringVar(value="00")
        self.second_string = tk.StringVar(value="00")
        self.lbf_input_time = ttk.LabelFrame(self, text="Enter Time", padding=5)
        self.lbl_hours = ttk.Label(self.lbf_input_time, text="Hours")
        self.lbl_minutes = ttk.Label(self.lbf_input_time, text="Minutes")
        self.lbl_seconds = ttk.Label(self.lbf_input_time, text="Seconds")
        self.txt_hours = self.create_time_entry(
            self.lbf_input_time, self.hour_string, 0
        )
        self.txt_minutes = self.create_time_entry(
            self.lbf_input_time, self.minute_string, 1
        )
        self.txt_seconds = self.create_time_entry(
            self.lbf_input_time, self.second_string, 2
        )
        self.prg_time_left = ttk.Progressbar(self.lbf_input_time)
        self.btn_start_timer = ttk.Button(
            self, text="Start Timer", command=self.run_timer, padding=5
        )

        self.setup_ui()
        self.should_stop_countdown = False

    def setup_window(self):
        """Set up the main application window."""
        self.title("NightWatch")
        self.resizable(height=False, width=False)

        # Calculate the x and y coordinates for the center of the screen
        width, height = 252, 275
        screen_width, screen_height = (
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )
        x, y = (screen_width / 2) - (width / 2), (screen_height / 2) - (height / 2)
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

        self.iconbitmap(resource_path("icon.ico"))
        sv_ttk.set_theme("dark")  # Use 'Sun Valley' theme

    def setup_ui(self):
        """Set up the user interface elements."""
        # setup action section
        self.lbf_action.grid(row=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.cmb_actions.current(0)
        self.cmb_actions.bind(
            "<<ComboboxSelected>>", lambda _: self.cmb_actions.selection_clear()
        )
        self.cmb_actions.grid(row=0, padx=6, pady=10, sticky="ew")

        # setup time input section
        self.lbf_input_time.grid(row=1, columnspan=3, padx=10, pady=0, sticky="ew")
        self.lbl_hours.grid(column=0, row=0, padx=10, pady=5)
        self.lbl_minutes.grid(column=1, row=0, padx=10, pady=5)
        self.lbl_seconds.grid(column=2, row=0, padx=10, pady=5)
        self.prg_time_left.grid(row=5, columnspan=3, padx=10, pady=10, sticky="ew")

        self.btn_start_timer.grid(row=6, columnspan=3, padx=10, pady=10, sticky="ew")

    def create_time_entry(self, parent, string_var, column):
        """Create a time entry widget."""
        entry = ttk.Entry(parent, width=3, textvariable=string_var, justify="center")
        entry.bind("<FocusIn>", lambda event: event.widget.select_range(0, "end"))
        entry.grid(column=column, row=1, padx=15, pady=5)
        return entry

    def run_timer(self):
        """Start the timer based on user input."""
        try:
            clock_time = (
                int(self.hour_string.get()) * 3600
                + int(self.minute_string.get()) * 60
                + int(self.second_string.get())
            )
            set_time = clock_time
            self.should_stop_countdown = False
        except ValueError:
            self.show_error("Invalid values")
            return

        if clock_time <= 0:
            self.show_error("A positive number is required")
            return

        def stop_countdown():
            self.should_stop_countdown = True

        self.btn_start_timer.config(text="Cancel", command=stop_countdown)

        self.countdown(clock_time, set_time)

    def show_error(self, message):
        """Display an error message in a message box."""
        logging.error("Error: %s", message)
        messagebox.showinfo("NightWatch", message, icon="error")

    def countdown(self, clock_time, set_time):
        """Perform the countdown and update the UI accordingly."""
        self.should_stop_countdown = False

        def tick():
            nonlocal clock_time
            self.update()

            if self.should_stop_countdown:
                self.reset_timer(set_time)
                return

            total_minutes, total_seconds = divmod(clock_time, 60)
            total_hours, total_minutes = divmod(total_minutes, 60)

            self.hour_string.set(f"{total_hours:02d}")
            self.minute_string.set(f"{total_minutes:02d}")
            self.second_string.set(f"{total_seconds:02d}")

            self.prg_time_left.configure(value=clock_time, maximum=set_time)
            logging.debug(clock_time, "seconds left")
            self.update()

            if clock_time > 0:
                clock_time -= 1
                self.after(1000, tick)
            else:
                self.execute_action()

        tick()

    def reset_timer(self, set_time):
        """Reset the timer to its initial state."""
        self.hour_string.set("00")
        self.minute_string.set("00")
        self.second_string.set("00")
        self.prg_time_left.configure(value=0, maximum=set_time)
        self.update()
        logging.info("Timer has been cancelled")
        self.btn_start_timer.config(text="Start Timer", command=self.run_timer)

    def execute_action(self):
        """Execute the selected action after the countdown ends."""
        action = self.cmb_actions.get()
        if action == "Pause":
            pause_media()
        elif action == "Sleep":
            sleep_system(self)
        elif action == "Shutdown":
            shutdown_system(self)
        else:
            self.show_error("No action selected")
        self.btn_start_timer.config(text="Start Timer", command=self.run_timer)


if __name__ == "__main__":
    NightWatch().mainloop()
