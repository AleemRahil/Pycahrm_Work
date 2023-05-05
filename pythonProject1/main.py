from turtle import Turtle, Screen
import random
from scoreboard import Score
from paddle import Paddle
from ball import Ball
import time

PADDLE_POSITIONS = [(-350, 0), (350, 0)]

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Ping Pong")
screen.tracer(0)

screen.listen()

paddle_l = Paddle(PADDLE_POSITIONS[0])
paddle_r = Paddle(PADDLE_POSITIONS[1])

screen.onkey(paddle_l.go_up, "w")
screen.onkey(paddle_l.go_down, "s")
screen.onkey(paddle_r.go_up, "Up")
screen.onkey(paddle_r.go_down, "Down")

score =  Score()
ball = Ball()
game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    ball.move()

    if ball.ycor() > 300 or ball.ycor() < -300:
        ball.bounce_y()

    if ball.distance(paddle_l) < 50 and ball.xcor() < -320 or ball.distance(paddle_r) < 50 and ball.xcor() > 320:
        ball.bounce_x()

    if ball.xcor() > 380:
        ball.reset_position()
        score.l_point()

    if ball.xcor() < -380:
        ball.reset_position()
        score.r_point()





screen.exitonclick()