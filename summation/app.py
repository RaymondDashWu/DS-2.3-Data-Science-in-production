
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, FloatField, validators

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'

# Simple Flask server setup to add one number to another.
class Addition(FlaskForm):
    number1 = FloatField('Number1')
    number2 = FloatField('Number2')

@app.route('/', methods=['GET', 'POST'])
def form():
    form = Addition()
    if form.validate_on_submit():
        return str(form.number1.data + form.number2.data)
    return render_template('addition.html', form=form)

if __name__ == '__main__':
    app.run(debug = True)