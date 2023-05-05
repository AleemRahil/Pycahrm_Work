from turtle import Turtle


class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.ball = Turtle()
        self.ball.shape("circle")
        self.ball.color("white")
        self.ball.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1

    def move(self):
        new_x = self.ball.xcor() + self.x_move
        new_y = self.ball.ycor() + self.y_move
        self.ball.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1
        self.move_speed *= 0.9

    def ball_collision(self):
        self.bounce_x()

    def ball_out(self):
        self.reset_position()
        self.bounce_x()
        self.bounce_y()
        self.move_speed = 0.1

    def ball_in(self):
        self.bounce_x()
        self.bounce_y()
        self.move_speed = 0.1



    def reset_position(self):
        self.ball.goto(0,0)
        self.move_speed = 0.1
        self.bounce_x()
