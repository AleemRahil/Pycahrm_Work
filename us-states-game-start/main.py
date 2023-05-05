import pandas as pd
import turtle

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

data = pd.read_csv("50_states.csv")
states_list = data["state"].to_list()
score = 0
correct_states = []

for _ in range(50):
    state_name = screen.textinput(f"{len(correct_states)}/50 Guessed Correct",
                                  "What's another state's name?").title()
    if state_name.title() == "Exit":
        missing_states = [state for state in states_list if state not in correct_states]
        new_data = pd.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break
    if state_name.title() in states_list:
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data["state"] == state_name.title()]
        t.goto(int(state_data["x"]), int(state_data["y"]))
        t.write(state_name.title())
        score+=1
        correct_states.append(state_name.title())

