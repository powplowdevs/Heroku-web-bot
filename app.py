# from flask import Flask, render_template, request, flash

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# # main driver function
# if __name__ == '__main__':
 
#     # run() method of Flask class runs the application
#     # on the local development server.
#     app.run()

import os
import requests
from lxml import html

from flask import request
from flask import Flask
from flask import Response


app = Flask(__name__)


@app.route('/')
def home():
    usage = 'Pass a properly encoded url parameter e.g. /https/www.google.com'
    return usage

@app.route('/https/<url>')
def root(url):    
    url = 'https://' + url
    print(url)
    r = requests.get(url)
    rr = Response(response=r.content, status=r.status_code)
    rr.headers["Content-Type"] = r.headers['Content-Type']
    return rr

@app.route('/g/<keyword>')
def gkeyword(keyword):     
    url = 'https://www.google.com/search?q='
    print(url)
    payload = {'q':keyword, 'num':1, 'start':1, 'sourceid':'chrome', 'ie':'UTF-8', 'cr':'cr=countryUS'}
    r = requests.get(url, params=payload)
    rr = Response(response=r.content, status=r.status_code)
    rr.headers["Content-Type"] = r.headers['Content-Type']
    return rr

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 8000.
    #port = int(os.environ.get('PORT', 8000))
    app.run()
