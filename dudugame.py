import tkinter as tk
import random


class WhackAMole:
    def __init__(self, root):
        self.root = root
        self.root.title("Whack-A-Mole")

        self.canvas = tk.Canvas(root, width=500, height=500, bg="beige")
        self.canvas.pack()

        self.score = 0
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack()

        self.chapter_label = tk.Label(root, text="Chapter: 1", font=("Arial", 16))
        self.chapter_label.pack()

        self.mole = None
        self.running = False

        self.start_button = tk.Button(
            root, text="Start Game", font=("Arial", 16), command=self.start_game
        )
        self.start_button.place(x=250, y=250, anchor="center")

        self.chapters = [
            {"speed": 1500, "moles": 10},
            {"speed": 1300, "moles": 10},
            {"speed": 1100, "moles": 10},
            {"speed": 900, "moles": 10},
            {"speed": 800, "moles": 10},
        ]
        self.current_chapter = 0
        self.successful_hits = 0

    def start_game(self):
        self.start_button.place_forget()
        self.score = 0
        self.successful_hits = 0
        self.running = True
        self.current_chapter = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.chapter_label.config(text="Chapter: 1")
        self.start_chapter()

    def start_chapter(self):
        chapter = self.chapters[self.current_chapter]
        self.successful_hits = 0
        self.create_mole(chapter["speed"])

    def create_mole(self, speed):
        if not self.running or self.successful_hits >= 10:
            self.check_next_chapter()
            return

        x = random.randint(50, 450)
        y = random.randint(50, 450)
        self.mole = self.canvas.create_oval(x - 50, y - 50, x + 50, y + 50, fill="brown")
        self.mole_coords = (x - 50, y - 50, x + 50, y + 50)

        self.canvas.tag_bind(self.mole, "<Button-1>", self.hit_mole)
        self.canvas.bind("<Button-1>", self.fail_game)

        self.root.after(speed, self.auto_fail)
        self.root.after(speed, self.create_mole, speed)

    def hit_mole(self, event):
        if self.running and self.mole:
            x_click, y_click = event.x, event.y
            if self.mole_coords[0] <= x_click <= self.mole_coords[2] and self.mole_coords[1] <= y_click <= self.mole_coords[3]:
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.canvas.delete(self.mole)
                self.mole = None
                self.successful_hits += 1
            else:
                self.fail_game(event)

    def fail_game(self, event):
        if self.running and self.mole:
            x_click, y_click = event.x, event.y
            if not (self.mole_coords[0] <= x_click <= self.mole_coords[2] and self.mole_coords[1] <= y_click <= self.mole_coords[3]):
                self.running = False
                if self.mole:
                    self.canvas.delete(self.mole)
                self.mole = None
                self.score_label.config(text=f"Game Over! Final Score: {self.score}")
                self.chapter_label.config(text="Fail!")

                fail_label = tk.Label(self.root, text="Fail", font=("Arial", 30), fg="red")
                fail_label.place(x=250, y=150, anchor="center")

                self.root.after(3000, self.show_start_screen)

    def auto_fail(self):
        if self.running and self.mole:
            self.running = False
            self.canvas.delete(self.mole)
            self.mole = None
            self.score_label.config(text=f"Game Over! Final Score: {self.score}")
            self.chapter_label.config(text="Fail!")

            fail_label = tk.Label(self.root, text="Fail", font=("Arial", 30), fg="red")
            fail_label.place(x=250, y=150, anchor="center")

            self.root.after(3000, self.show_start_screen)

    def check_next_chapter(self):
        if self.successful_hits < 10:
            return

        if self.current_chapter + 1 < len(self.chapters):
            self.current_chapter += 1
            chapter = self.chapters[self.current_chapter]
            self.chapter_label.config(text=f"Chapter: {self.current_chapter + 1}")
            self.start_chapter()
        else:
            self.end_game()

    def end_game(self):
        self.running = False
        if self.mole:
            self.canvas.delete(self.mole)
        self.mole = None
        self.score_label.config(text=f"Game Over! Final Score: {self.score}")
        self.chapter_label.config(text="All Chapters Completed!")

        self.root.after(3000, self.show_start_screen)

    def show_start_screen(self):
        for widget in self.root.winfo_children():
            widget.place_forget()
        self.start_button.place(x=250, y=250, anchor="center")


if __name__ == "__main__":
    root = tk.Tk()
    game = WhackAMole(root)
    root.mainloop()
