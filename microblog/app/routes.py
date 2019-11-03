from app import app
from app.forms import ConditionForm
from flask import render_template, flash, redirect, url_for
from flask_pymongo import pymongo

client = pymongo.MongoClient("mongodb+srv://aliu:aliu@hackduke2019-nkevk.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.test_database

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

@app.route('/')
@app.route('/condition', methods=['GET', 'POST'])
def condition():
    for entry in client.test_database.find():
        print(entry)
    form = ConditionForm()
    if form.validate_on_submit():
        flash('Condition={}, remember_me={}'.format(
            form.condition.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('condition.html', title='Sign In', form=form)
