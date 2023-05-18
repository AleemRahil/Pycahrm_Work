from random import randint
from flask import Flask

rand_num = randint(0, 9)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1 style="text-align: center">Guess a number between 0 and 9</h1>' \
                                        '<p>Kya Randi Rona laga rkha hei</p>' \
                                        '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">'

@app.route('/<int:user_num>')
def greet(user_num):
    if user_num == rand_num:
        return f'<h1 style="text-align: center">Congratulations! You guessed the correct number: {user_num}</h1>' \
               '<img src="https://media.giphy.com/media/effWdr0sDjXKy9uOoH/giphy.gif">'
    elif user_num > rand_num:
        return f'<h1 style="text-align: center">Wrong guess! The correct number was: {rand_num}</h1>' \
               '<img src="https://media.giphy.com/media/nqfN2oqtT4k8PNKzg1/giphy.gif">'
    elif user_num < rand_num:
        return f'<h1 style="text-align: center">Wrong guess! The correct number was: {rand_num}</h1>' \
               '<img src="https://media.giphy.com/media/nqfN2oqtT4k8PNKzg1/giphy.gif">'

if __name__ == '__main__':
    app.run()



