import random
import tkinter
import pandas
BACKGROUND_COLOR = "#B1DDC6"

try:
    french_english_words = pandas.read_csv("./data/learnt_french_words.csv")
except FileNotFoundError:
    french_english_words = pandas.read_csv("./data/french_words.csv")
    french_english_dict = french_english_words.to_dict(orient="records")
else:
    french_english_dict = french_english_words.to_dict(orient="records")


current_card = {}

def next_card():
    global current_card
    current_card= random.choice(french_english_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card, image=card_front_img)
    window.after(3000, func=flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card, image=card_back_img)

def  is_known():
    french_english_dict.remove(current_card)
    data = pandas.DataFrame(french_english_dict)
    data.to_csv("./data/learnt_french_words.csv", index=False)
    next_card()


window = tkinter.Tk()
window.title("Flashy")
window.configure(bg=BACKGROUND_COLOR, padx=50, pady=50)
canvas = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR)
card_front_img = tkinter.PhotoImage(file="./images/card_front.png")
card_back_img = tkinter.PhotoImage(file="./images/card_back.png")
card = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
cancel_button_image = tkinter.PhotoImage(file="./images/wrong.png")
cancel_button = tkinter.Button(image=cancel_button_image, highlightthickness=0, command=next_card)
cancel_button.grid(row=1, column=0)
correct_button_image = tkinter.PhotoImage(file="./images/right.png")
correct_button = tkinter.Button(image=correct_button_image, highlightthickness=0, command=is_known)
correct_button.grid(row=1, column=1)


window.mainloop()