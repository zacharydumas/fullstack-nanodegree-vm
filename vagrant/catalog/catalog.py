#!/usr/bin/env python2
#
#
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from catalog_database import Base, User, CatalogItem

app = Flask(__name__)


@app.route('/', methods=['GET'])
def catalog():
    return 'hello world'
















if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)