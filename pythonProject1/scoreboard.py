from turtle import Turtle
SCORE_POSITION = (0, 260)


class Score:

    def __init__(self):
        self.l_score = 0
        self.r_score = 0
        self.score_board = Turtle()
        self.score_board.color("white")
        self.score_board.penup()
        self.score_board.hideturtle()
        self.score_board.goto(SCORE_POSITION)
        self.update_score()

    def update_score(self):
        self.score_board.clear()
        self.score_board.write(f"Score: {self.l_score} | {self.r_score}", align="center", font=("Courier", 24, "normal"))

    def l_point(self):
        self.l_score += 1
        self.update_score()

    def r_point(self):
        self.r_score += 1
        self.update_score()