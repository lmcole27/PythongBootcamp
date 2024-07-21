from flask import Flask, render_template, request
import requests
import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()


msg = EmailMessage()
msg["subject"] = "New Account"
msg["from"] = os.environ.get("FROM_EMAIL")
msg["to"] = os.environ.get("TO_EMAIL")
sender_email_password = os.environ.get("FROM_EMAIL_PASSWORD")

blog_data = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html", blog_data=blog_data)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        msg.set_content(f"Subject: New account\nName: {request.form['name']}\nEmail: {request.form['email']}\nPhone: {request.form['phone']}\nMessage: {request.form['message']}")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(msg["from"], sender_email_password)
            server.send_message(msg)
        return render_template("contact.html", sent=True)
    else:
        return render_template("contact.html", sent=False)

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/form-entry', methods=["POST"])
def entry():
    print("I did it!")
    if request.method == "POST":
        return "<h1>Successfully sent message</h1>"
    else:
        return render_template("contact.html")


@app.route('/<int:index>')
def show_post(index):
    display_post = {}
    for blog in blog_data:
        if int(index) == int(blog['id']):
            display_post = blog
            return render_template("post.html", blog=display_post)
        else:
            pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

