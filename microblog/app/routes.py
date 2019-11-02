from flask import render_template
from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts  = [
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
        return redirect('/index')
    return render_template('condition.html', title='Condition', form=form)    

# @app.route