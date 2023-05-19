from flask import Flask, render_template
import datetime as t
import requests

time_now=t.datetime.now().year
response = requests.get('https://api.agify.io?name=michael')
dict=response.json()['age']

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', time=time_now, dict=dict)

@app.route('/blog/<num>')
def blog(num):

    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    all_posts=response.json()

    return render_template('blog.html', all_posts=all_posts )

if __name__ == '__main__':
    app.run()
