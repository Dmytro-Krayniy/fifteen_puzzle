from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from game import Game


def validate_username(form, username):
    s = username.data
    if not s[0].isupper():
        raise ValidationError('Name should start with a capital letter')
    for char in s:
        if char in '*?!"^+%&/()=}][{$#':
            raise ValidationError(f'Character {char} is not allowed in username')

class InitForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired(), Length(2, 50), validate_username])
    size = SelectField(
        'Please select size of puzzle',
        choices=[
            (2, 'First time 2 * 2'),
            (3, 'Beginner 3 * 3'),
            (4, 'Classic 4 * 4')
        ],
        default=4,
        coerce=int,
        render_kw={
            'class': 'form-control'
        }
    )
    labels = SelectField(
        'Please select type of items',
        choices=[
            (0, 'Figures 1, 2, 3, ..., 15'),
            (1, 'Letters A, B, C, ..., O')
        ],
        coerce=int,
        default=0,
        render_kw={
            'class': 'form-control'
        }
    )
    submit = SubmitField('Start')



class ArrowsForm(FlaskForm):
    up = SubmitField('UP')
    down = SubmitField('DOWN')
    left = SubmitField('LEFT')
    right = SubmitField('RIGHT')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'


@app.route('/', methods=['get', 'post'])
@app.route('/index', methods=['get', 'post'])
def index():
    form = InitForm()
    if form.validate_on_submit():
        name = form.name.data
        size = form.size.data
        labels = form.labels.data
        game = Game(height=size, width=size)
        return redirect('/game/' + name)

    return render_template('index.html', form=form)


@app.route('/game', methods=['get', 'post'])
@app.route('/game/<name>', methods=['get', 'post'])
def run_game(name):
    game = Game()
    arrows_form = ArrowsForm()
    if arrows_form.validate_on_submit():
        if arrows_form.up.data:
            game.form_new_turn('up')
        if arrows_form.down.data:
            game.form_new_turn('down')
        if arrows_form.left.data:
            game.form_new_turn('left')
        if arrows_form.right.data:
            game.form_new_turn('right')

    return render_template('game.html', game=game, form=arrows_form, name=name)


if __name__ == '__main__':
    app.run(debug=True)
