from turtle import Turtle

SNAKE_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20


class Snake:

    def __init__(self):
        self.snake_heads = []
        self.create_snake()

    def create_snake(self):
        for position in SNAKE_POSITIONS:
            snake_head = Turtle("square")
            snake_head.color("white")
            snake_head.penup()
            snake_head.goto(position)
            self.snake_heads.append(snake_head)

    def move(self):
        for snake_segment in range(len(self.snake_heads) - 1, 0, -1):
            new_x = self.snake_heads[snake_segment - 1].xcor()
            new_y = self.snake_heads[snake_segment - 1].ycor()
            self.snake_heads[snake_segment].goto(new_x, new_y)
        self.snake_heads[0].forward(MOVE_DISTANCE)

    def up(self):
        if self.snake_heads[0].heading() != 270:
            self.snake_heads[0].setheading(90)

    def down(self):
        if self.snake_heads[0].heading() != 90:
            self.snake_heads[0].setheading(270)

    def left(self):
        if self.snake_heads[0].heading() != 0:
            self.snake_heads[0].setheading(180)

    def right(self):
        if self.snake_heads[0].heading() != 180:
            self.snake_heads[0].setheading(0)

    def extend(self):
        self.add_snake_segment(self.snake_heads[-1].position())

    def add_snake_segment(self, position):
        snake_segment = Turtle("square")
        snake_segment.color("white")
        snake_segment.penup()
        snake_segment.goto(position)
        self.snake_heads.append(snake_segment)

    def reset(self):
        for snake_segment in self.snake_heads:
            snake_segment.goto(1000, 1000)
        self.snake_heads.clear()
        self.create_snake()

    def collision_with_wall(self):
        if self.snake_heads[0].xcor() > 280 or self.snake_heads[0].xcor() < -280 or self.snake_heads[0].ycor() > 280 or \
                self.snake_heads[0].ycor() < -280:
            return True
        else:
            return False

    def collision_with_tail(self):
        for snake_segment in self.snake_heads[1:]:
            if self.snake_heads[0].distance(snake_segment) < 10:
                return True
        return False

    def collision_with_food(self, food):
        if self.snake_heads[0].distance(food) < 10:
            return True
        else:
            return False


