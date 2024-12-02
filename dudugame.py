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

        # 챕터 설정: 속도를 느리게 조정
        self.chapters = [
            {"speed": 1500, "moles": 10},
            {"speed": 1300, "moles": 10},
            {"speed": 1100, "moles": 10},
            {"speed": 900, "moles": 10},
            {"speed": 800, "moles": 10},
        ]
        self.current_chapter = 0
        self.successful_hits = 0  # 각 챕터에서 성공적으로 맞춘 두더지 수

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
        self.successful_hits = 0  # 챕터 시작 시 성공적인 두더지 횟수 초기화
        self.create_mole(chapter["speed"])

    def create_mole(self, speed):
        if not self.running or self.successful_hits >= 10:
            self.check_next_chapter()
            return

        # 두더지 생성 후 일정 시간 후 다시 생성
        x = random.randint(50, 450)
        y = random.randint(50, 450)
        self.mole = self.canvas.create_oval(x - 50, y - 50, x + 50, y + 50, fill="brown")  # 색상 수정
        self.mole_coords = (x - 50, y - 50, x + 50, y + 50)  # 원의 좌표 저장

        self.canvas.tag_bind(self.mole, "<Button-1>", self.hit_mole)

        # 화면 전체에 클릭 이벤트를 바인딩해서 두더지를 클릭하지 않으면 실패 처리
        self.canvas.bind("<Button-1>", self.fail_game)

        # 일정 시간 후에 두더지를 삭제하고 Fail 화면을 띄움
        self.root.after(speed, self.auto_fail)
        
        # 일정 시간 후 다시 두더지 생성
        self.root.after(speed, self.create_mole, speed)

    def hit_mole(self, event):
        if self.running and self.mole:
            # 클릭된 좌표가 두더지 영역 안에 있으면 성공
            x_click, y_click = event.x, event.y
            if self.mole_coords[0] <= x_click <= self.mole_coords[2] and self.mole_coords[1] <= y_click <= self.mole_coords[3]:
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.canvas.delete(self.mole)
                self.mole = None
                self.successful_hits += 1  # 성공적인 두더지 클릭 증가
            else:
                self.fail_game(event)  # 클릭이 잘못된 곳이라면 실패 처리

    def fail_game(self, event):
        if self.running and self.mole:  # 두더지가 있을 때만 실패 처리
            x_click, y_click = event.x, event.y
            if not (self.mole_coords[0] <= x_click <= self.mole_coords[2] and self.mole_coords[1] <= y_click <= self.mole_coords[3]):
                self.running = False
                if self.mole:
                    self.canvas.delete(self.mole)
                self.mole = None
                self.score_label.config(text=f"Game Over! Final Score: {self.score}")
                self.chapter_label.config(text="Fail!")

                # "Fail" 화면 띄우기
                fail_label = tk.Label(self.root, text="Fail", font=("Arial", 30), fg="red")
                fail_label.place(x=250, y=150, anchor="center")

                # 3초 후에 게임 스타트 화면으로 돌아가기
                self.root.after(3000, self.show_start_screen)

    def auto_fail(self):
        if self.running and self.mole:  # 일정 시간 후 두더지가 클릭되지 않았다면
            self.running = False
            self.canvas.delete(self.mole)
            self.mole = None
            self.score_label.config(text=f"Game Over! Final Score: {self.score}")
            self.chapter_label.config(text="Fail!")

            # "Fail" 화면 띄우기
            fail_label = tk.Label(self.root, text="Fail", font=("Arial", 30), fg="red")
            fail_label.place(x=250, y=150, anchor="center")

            # 3초 후에 게임 스타트 화면으로 돌아가기
            self.root.after(3000, self.show_start_screen)

    def check_next_chapter(self):
        if self.successful_hits < 10:
            return  # 아직 10개를 맞추지 않았으므로 계속 진행

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
        
        # 3초 후에 게임 스타트 화면으로 돌아가기
        self.root.after(3000, self.show_start_screen)

    def show_start_screen(self):
        # Fail 화면을 삭제하고 시작 화면으로 돌아감
        for widget in self.root.winfo_children():
            widget.place_forget()
        self.start_button.place(x=250, y=250, anchor="center")


if __name__ == "__main__":
    root = tk.Tk()
    game = WhackAMole(root)
    root.mainloop()
