#!/usr/bin/env python2
#
#
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from catalog_database import Base, User, CatalogItem

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
        item = session.query(CatalogItem).filter_by(category = category, name = item).one()
    return render_template('catalog_new.html', categories = categories, entry = item, items = items)

# GET displays the page to create a new item, POST adds a new item to the database
@app.route('/<category>/new', methods = ['GET','POST'])
def createItem(category):
    return 'GET displays the page to create a new item, POST adds a new item to the database'

# GET displays the page to edit a item, POST edits an item in the database
@app.route('/<category>/<item>/edit', methods = ['GET','POST'])
def editItem(category,item):
    return 'GET displays the page to edit a item, POST edits an item in the database'

# GET displays a confirmation page to delete an item, POST deletes the item
@app.route('/<category>/<item>/delete', methods = ['GET','POST'])
def deleteItem(category,item):
    return 'GET displays a confirmation page to delete an item, POST deletes the item'

# API -----------------------------------------------------
# GET returns a json object of the categories
@app.route('/api/v1')
def catalogJson():
    return 'GET returns a json object of the categories'

# GET returns a json object of the items within a category
@app.route('/api/v1/<category>')
def categoryJson(category):
    return 'GET returns a json object of the items within a category'

# GET returns a json object of an item
@app.route('/api/v1/<category>/<item>')
def itemJson(category,item):
    item = session.query(CatalogItem).filter_by(category = category, name = item).one()
    return jsonify(item.serialize)

# Authentication --------------------------------------------
# POST logs the user in 
@app.route('/connect', methods = ['POST'])
def connect():
    return 'log a user in'

# POST logs a user out
@app.route('/disconnect', methods = ['POST'])
def disconnect():
    return 'log a user out'

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)