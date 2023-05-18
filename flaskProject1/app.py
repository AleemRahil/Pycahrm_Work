from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/generic.html')
def hello_world2():  # put application's code here
    return render_template('generic.html')

@app.route('/elements.html')
def hello_world3():  # put application's code here
    return render_template('elements.html')

if __name__ == '__main__':
    app.run()
