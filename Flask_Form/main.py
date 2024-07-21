from flask_bootstrap import Bootstrap5

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email


class MyForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired("Please enter email"), Email("email Yo!"), Length(8)])
    password = PasswordField('Password', validators=[InputRequired("Password Yo"), Length(8)])
    submit = SubmitField('LogIn', validators=[InputRequired()])

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = 'My_Secret_Key'

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = MyForm()
    form.validate_on_submit()
    return render_template('login.html', form=form)
    
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return render_template('success.html')
    return render_template('denied.html')

if __name__ == '__main__':
    app.run(debug=True)
