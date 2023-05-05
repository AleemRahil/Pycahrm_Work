from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.tracer(0)
screen.title("My Snake Game")
sleep_time = 0.1
snake = Snake()
food = Food()
score = Scoreboard()
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

screen.update()

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(sleep_time)
    score.update_scoreboard()
    snake.move()
    if snake.collision_with_food(food):
        food.refresh()
        snake.extend()
        score.increase_score()
        sleep_time += 0.001
    if snake.collision_with_wall():
        score.reset()
        snake.reset()
        food.refresh()


    if snake.collision_with_tail():
        score.reset()
        snake.reset()
        food.refresh()


screen.exitonclick()
