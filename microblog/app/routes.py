from flask import render_template
from app import app
from app.forms import ConditionForm
from flask import render_template, flash, redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }

    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/condition')
def condition():
    form = ConditionForm()
    if form.validate_on_submit():
        flash('Condition={} requested, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('condition.html', title='Sign In', form=form)
