from app import app
from app.forms import ConditionForm
from flask import render_template, flash, redirect, url_for, request
from flask_pymongo import pymongo
import requests

client = pymongo.MongoClient("mongodb+srv://aliu:aliu@hackduke2019-nkevk.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.inline
hospitalList = db.HospitalCost.find()

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

@app.route('/condition', methods=['GET', 'POST'])
def condition():
    #return render_template('condition.html', title='Condition')
    form = ConditionForm()
    if form.validate_on_submit():
        flash('Condition={}, remember_me={}'.format(
            form.condition.data, form.remember_me.data))
        return redirect(url_for('hospitals'))
    return render_template('condition.html', title='Condition', form=form)
    

@app.route('/hospitals')
def hospitals():
    return render_template('hospitals.html', title='Hospitals', hospitals=hospitalList)