from flask import Flask, render_template, url_for
import requests

class Blog:
    def __init__(self, post_id, title, subtitle, body):
        self.id = post_id
        self.title = title
        self.subtitle = subtitle
        self.body = body

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

post_list = []
for post in posts:
    new_post = Blog(post["id"], post["title"], post["subtitle"], post["body"])
    post_list.append(new_post)


app = Flask(__name__)

@app.route('/')
def home():    
    return render_template("index.html", posts = post_list)

@app.route("/post/<int:index>")
def show_post(index):
    display_post = {}
    for post in posts:
        if post["id"] == int(index):
            display_post = post
    return render_template("post.html", display_post=display_post)

if __name__ == "__main__":
    app.run(debug=True)
