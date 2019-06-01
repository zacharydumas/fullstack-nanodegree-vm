#!/usr/bin/env python2
#
#
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from catalog_database import Base, User, CatalogItem

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import json

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Displays the description of an item if an item is provited, otherwise displays a list of items 
# within the requested category if a category is provided, otherwise displays the latest 10 items
@app.route('/')
@app.route('/<category>')
@app.route('/<category>/<item>')
def showCategory(category = None, item = None):
    query = session.query(CatalogItem.category.distinct().label('category')).order_by(asc(CatalogItem.category))
    categories = [row.category for row in query.all()]
    if category != None:
        items = session.query(CatalogItem).filter_by(category = category).order_by(asc(CatalogItem.name))
    else:
        items = session.query(CatalogItem).order_by(desc(CatalogItem.id)).limit(10).all()
    if item != None:
        item = session.query(CatalogItem).filter_by(category = category, name = item).limit(1).one()
    return render_template('catalog_new.html', categories = categories, entry = item, items = items)

# GET displays the page to create a new item, POST adds a new item to the database
@app.route('/new', methods = ['GET','POST'])
def createItem():
    if request.method == 'POST':
        email = "placeholder@gmail.com"
        newItem = CatalogItem(name = request.form['name'], description = request.form['description'], category = request.form['category'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategory', category = request.form['category'], item = request.form['name']))
    else:
        return render_template('createItem.html')

# GET displays the page to edit a item, POST edits an item in the database
@app.route('/<category>/<item>/edit', methods = ['GET','POST'])
def editItem(category,item):
    if request.method == 'POST':
        pass
    else:
        return render_template('editItem.html')

# GET displays a confirmation page to delete an item, POST deletes the item
@app.route('/<category>/<item>/delete', methods = ['GET','POST'])
def deleteItem(category,item):
    if request.method == 'POST':
        item = session.query(CatalogItem).filter_by(category = category, name = item).limit(1).one()
        session.delete(item)
        session.commit()
        return redirect(url_for('showCategory'))
    else:
        return render_template('deleteItem.html', category = category, item = item)

# API -----------------------------------------------------
# GET returns a json object of the categories
@app.route('/api/v1')
def catalogJson():
    query = session.query(CatalogItem).order_by(asc(CatalogItem.name))
    items = query.all()
    return jsonify([item.serialize for item in items])

# GET returns a json object of the items within a category
@app.route('/api/v1/<category>')
def categoryJson(category):
    query = session.query(CatalogItem).filter_by(category = category).order_by(asc(CatalogItem.name))
    items = query.all()
    return jsonify([item.serialize for item in items])

# GET returns a json object of an item
@app.route('/api/v1/<category>/<item>')
def itemJson(category,item):
    item = session.query(CatalogItem).filter_by(category = category, name = item).one()
    return jsonify(item.serialize)

# Authentication --------------------------------------------
# redirect the user to OAuth provider
@app.route('/login')
def login():
    flow = flow_from_clientsecrets('client_secrets.json', scope='https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',redirect_uri=url_for('connect', _external=True))
    return redirect(flow.step1_get_authorize_url())

# POST logs the user in 
@app.route('/connect', methods = ['Get','POST'])
def connect():
    flow = flow_from_clientsecrets('client_secrets.json', scope='https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',redirect_uri=url_for('connect', _external=True))
    try:
        code = request.args.get('code')
        if code == None:
            return "access was denied"     
        credentials = flow.step2_exchange(code)
    except FlowExchangeError:
        return "failed to aqcuire authorization"
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['name'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    return redirect(url_for('showCategory'))

# POST logs a user out
@app.route('/disconnect', methods = ['POST'])
def disconnect():
    return 'log a user out'

if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)