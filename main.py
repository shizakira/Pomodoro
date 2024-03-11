import time
import tkinter as tk
import threading
from tkinter import ttk, PhotoImage


class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x455")
        self.root.title("Pomodoro Timer Shizofreniya")

        self.root.tk.call('wm', 'iconphoto', self.root,
                          PhotoImage(file="qH_QZnh01xQ.png"))

        self.background_img = PhotoImage(file="MGaeyyp.png")
        self.background_label = tk.Label(self.root, image=self.background_img)
        self.background_label.place(x=0, y=0, relheight=1, relwidth=1)

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Comic Sans MS", 16))
        self.style.configure("TButton", font=("Comic Sans MS", 16), background="black")

        self.main_frame = ttk.Frame(self.root)
        self.timer_label = ttk.Label(self.main_frame,
                                     font=("Comic Sans MS", 34), text="25:00 Pomodor", relief="groove")
        self.timer_label.pack()
        self.main_frame.pack(anchor='w')

        self.grid_layout = ttk.Frame(self.root, relief="groove")
        self.grid_layout.pack(side=tk.BOTTOM, pady=(0, 10))

        self.pomodoros_counter_label = ttk.Label(self.grid_layout, text="Pomodoros: 0")
        self.pomodoros_counter_label.grid(row=1, column=0, columnspan=3, pady=10)

        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0)

        self.reset_button = ttk.Button(self.grid_layout, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=0, column=1)

        self.skip_button = ttk.Button(self.grid_layout, text="Skip", command=self.skip_time)
        self.skip_button.grid(row=0, column=2)

        self.running = False
        self.stopped = False
        self.skipped = False
        self.pomodoros = 0

        self.root.mainloop()

    def start_timer_thread(self):
        if not self.running:
            self.running = True
            self.timer_thread = threading.Thread(target=self.start_timer)
            self.timer_thread.start()

    def start_timer(self):
        self.stopped = False

        full_seconds = 60 * 25
        action = "Pomodor"
        while self.running:
            while full_seconds and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d} {action}")
                self.timer_label.update()
                time.sleep(1)
                if self.skipped:
                    full_seconds = 0
                else:
                    full_seconds -= 1

            self.skipped = False

            if action == "Pomodor":
                self.pomodoros += 1
                self.pomodoros_counter_label.configure(text=f"Pomodoros: {self.pomodoros}")
                self.pomodoros_counter_label.update()
                if self.pomodoros % 4 == 0:
                    full_seconds = 60 * 15
                    action = "Chill 15 minutes"
                else:
                    full_seconds = 60 * 5
                    action = "Chill 5 minutes"
            else:
                full_seconds = 60 * 25
                action = "Pomodor"

    def reset_timer(self):
        if self.running:
            self.running = False
            self.stopped = True

            self.pomodoros = 0
            self.pomodoros_counter_label.configure(text="Pomodoros: 0")
            self.pomodoros_counter_label.update()

            self.timer_label.configure(text="25:00 Pomodor")
            self.timer_label.update()

    def skip_time(self):
        if self.running:
            self.skipped = True


if __name__ == "__main__":
    PomodoroTimer()
