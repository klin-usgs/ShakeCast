from app.functions_util import *
from app.objects import AlchemyEncoder
import os
import sys
import json
modules_dir = sc_dir() + 'modules'
if modules_dir not in sys.path:
    sys.path += [modules_dir]

from flask import Flask, render_template, url_for, request
import time
import datetime
from app.dbi.db_alchemy import *
from app.server import Server
from app.functions_util import *
from app.objects import Clock
app = Flask(__name__,
            template_folder=sc_dir()+'view'+get_delim()+'html',
            static_folder=sc_dir()+'view'+get_delim()+'static')

@app.route('/')
def index():
    # make navbar
    navitems = [{'title': 'home',
                 'text': 'Home'},
                {'title': 'about',
                 'text': 'About Us'},
                {'title': 'contact',
                 'text': 'Contact Us'},
                {'title': 'earthquakes',
                  'text': 'Earthquakes'}]
    
    # get eq info
    session = Session()
    clock = Clock()
    eqs = session.query(Event).order_by(Event.time.desc())
    datetimes = []
    Session.remove()
    for eq in eqs:
        datetimes += [clock.from_time(eq.time).strftime('%Y-%m-%d %H:%M:%S')]
    return render_template('index.html', navitems=navitems, eqs_times=zip(eqs,datetimes))

@app.route('/earthquakes')
def earthquakes():
    return render_template('earthquakes.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/get/eqdata/')
def eq_data():
    session = Session()
    eqs = session.query(Event).order_by(Event.time.desc()).all()
    eq_json = json.dumps(eqs, cls=AlchemyEncoder)
    
    return eq_json

@app.route('/dbtest')
def db_test():
    session = Session()
    
    eqs = session.query(ShakeMap).all()
    eqs = eqs[-10:]
    
    return_str = 'Recent EQs:\n'
    return_str += str([str(eq) for eq in eqs])

    return return_str
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-d':
            # run in debug mode
            app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=80)