from flask import Flask, render_template, request
from database import db_session
from models import User

app = Flask(__name__)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    user = User(name=name, email=email)
    db_session.add(user)
    db_session.commit()
    return 'User added successfully!'

if __name__ == '__main__':
    app.run()
