import tkinter as tk
from tkinter import messagebox
import time
from code_generator import CodeGenerator

COLOR_BG = "#FFFFFF"
COLOR_TABLET = "#9E9E9E"
COLOR_SCREEN = "#FFFFFF"
COLOR_HEADER = "#7B68EE"
COLOR_TARGET_BG = "#CFA935"
COLOR_BTN_BG = "#C0C0C0"
COLOR_BTN_TXT = "#000000"
COLOR_PROGRESS = "#76FF03"

class ZapNGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zap-N: Code Compare")
        self.root.geometry("600x600")
        self.root.configure(bg=COLOR_BG)

        self.generator = CodeGenerator()
        self.score = 0
        self.time_limit = 3.0
        self.start_time = 0
        self.timer_running = False
        self.current_target = ""

        self._setup_ui()
        self._show_start_screen()

    def _setup_ui(self):
        self.lbl_header = tk.Label(
            self.root, text="Zap-N", font=("Verdana", 24, "bold"), 
            fg=COLOR_HEADER, bg=COLOR_BG
        )
        self.lbl_header.pack(pady=(10, 5))

        self.tablet_frame = tk.Frame(
            self.root, bg=COLOR_TABLET, bd=0, 
            padx=20, pady=20
        )
        self.tablet_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        self.screen_frame = tk.Frame(self.tablet_frame, bg=COLOR_SCREEN)
        self.screen_frame.pack(expand=True, fill="both")

        self.lbl_title = tk.Label(
            self.screen_frame, text="CodeCompare", font=("Arial", 20, "bold"),
            bg=COLOR_SCREEN, fg="black"
        )
        self.lbl_title.pack(pady=(15, 5))

        self.progress_canvas = tk.Canvas(
            self.screen_frame, width=300, height=15, bg="#E0E0E0", highlightthickness=0
        )
        self.progress_canvas.pack(pady=5)
        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 300, 15, fill=COLOR_PROGRESS, outline="")

        self.lbl_score = tk.Label(
            self.screen_frame, text="Score: 0", font=("Arial", 10),
            bg=COLOR_SCREEN, fg="#555"
        )
        self.lbl_score.place(x=10, y=10)

        self.lbl_target = tk.Label(
            self.screen_frame, text="WAITING...", 
            font=("Courier New", 22, "bold"),
            bg=COLOR_TARGET_BG, fg="black",
            width=12, pady=5
        )
        self.lbl_target.pack(pady=(10, 15))

        self.options_container = tk.Frame(self.screen_frame, bg=COLOR_SCREEN)
        self.options_container.pack(fill="both", expand=True)

    def _show_start_screen(self):
        self._clear_options()
        btn_start = tk.Button(
            self.options_container, text="START GAME", 
            font=("Arial", 14, "bold"), bg=COLOR_PROGRESS, fg="black",
            command=self.start_game, relief="flat", padx=20, pady=10
        )
        btn_start.pack(pady=50)

    def _clear_options(self):
        for widget in self.options_container.winfo_children():
            widget.destroy()

    def start_game(self):
        self.score = 0
        self.generator = CodeGenerator()
        self.update_score_label()
        self.next_round()

    def next_round(self):
        self.timer_running = False
        self.current_target = self.generator.generate_code()
        options = self.generator.generate_answers(self.current_target)

        self.lbl_target.config(text=self.current_target)
        self._clear_options()

        for opt in options:
            btn = tk.Button(
                self.options_container, 
                text=opt, 
                font=("Courier New", 16, "bold"),
                bg=COLOR_BTN_BG, 
                fg=COLOR_BTN_TXT,
                activebackground="#A0A0A0",
                relief="flat",
                pady=5,
                width=15,
                command=lambda x=opt: self.check_answer(x)
            )
            btn.pack(pady=4)

        self.start_timer()

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self._animate_timer()

    def _animate_timer(self):
        if not self.timer_running:
            return

        current_time = time.time()
        elapsed = current_time - self.start_time
        remaining_ratio = 1 - (elapsed / self.time_limit)

        if remaining_ratio <= 0:
            self.timer_running = False
            self.progress_canvas.coords(self.progress_bar, 0, 0, 0, 15)
            self.game_over("Time's up!")
        else:
            new_width = 300 * remaining_ratio
            self.progress_canvas.coords(self.progress_bar, 0, 0, new_width, 15)
            
            if remaining_ratio < 0.3:
                self.progress_canvas.itemconfig(self.progress_bar, fill="#FF3D00")
            else:
                self.progress_canvas.itemconfig(self.progress_bar, fill=COLOR_PROGRESS)

            self.root.after(30, self._animate_timer)

    def check_answer(self, selected_code):
        if not self.timer_running:
            return

        if selected_code == self.current_target:
            self.score += 1
            self.update_score_label()
            self.next_round()
        else:
            self.timer_running = False
            self.game_over(f"Wrong code!\nSelected: {selected_code}\nExpected: {self.current_target}")

    def update_score_label(self):
        self.lbl_score.config(text=f"Score: {self.score}")

    def game_over(self, reason):
        messagebox.showinfo("GAME OVER", f"{reason}\n\nFinal Score: {self.score}")
        self._show_start_screen()
        self.progress_canvas.coords(self.progress_bar, 0, 0, 300, 15)
        self.progress_canvas.itemconfig(self.progress_bar, fill=COLOR_PROGRESS)
        self.lbl_target.config(text="GAME OVER")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZapNGameApp(root)
    root.mainloop()