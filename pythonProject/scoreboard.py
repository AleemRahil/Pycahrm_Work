from turtle import Turtle


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        with open("data.txt") as data:
            self.high_score = int(data.read())
        self.penup()
        self.hideturtle()
        self._score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(0, 280)
        self.write(f"Score: {self._score} High Score: {self.high_score}", align="center", font=("Courier", 20, "normal"))

    def increase_score(self):
        self._score += 1
        self.update_scoreboard()

    def reset(self):
        if self._score > self.high_score:
            self.high_score = self._score
            with open("data.txt", mode="w") as data:
                data.write(f"{self.high_score}")
        self._score = 0
        self.update_scoreboard()



    # def game_over(self):
    #     self.goto(0, 0)
    #     self.write("GAME OVER", align="center", font=("Courier", 20, "normal"))
