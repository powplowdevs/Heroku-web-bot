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

from flask import Flask
from flask import Response
from flask import request as re

app = Flask(__name__)


@app.route('/h')
def home():
    usage = 'Enter a valid URL into the serach bar after this URL such as -> /https/www.google.com'
    return usage

#BASIC URLS
@app.route('/h/<url>')
def root(url): 
    try:
        if url != "search":
            url = "https://" + url

            r = requests.get(url)
            print("Fecthing: " + str(r.url))
            rr = Response(response=r.content, status=r.status_code)
            print("RESPONE CODE" + str(r.status_code) + "\n")

            if str(r.status_code) == "404":
                url = "https://google.com/" + url
                print("Error fetching base url, new url is: " + url)
                r = requests.get(url)
                rr = Response(response=r.content, status=r.status_code)
                rr.headers["Content-Type"] = r.headers['Content-Type']
                return rr

            return rr
    except:
        if url != "https://client_204":
            print("Error fetching [" + url + "]\nFull url: https://www.google.com" + url)
            url = "https://www.google.com/" + url
            r = requests.get(url)
            print("\n\n\n\nRESPONE CODE" + str(r.status_code))
            rr = Response(response=r.content, status=r.status_code)
            rr.headers["Content-Type"] = r.headers['Content-Type']
            return rr
        else:
            print("return null")
            return ""

#SEARCH GOOGLE
@app.route('/search?ie=ISO-8859-1&hl=en&source=hp&biw=&bih=&q=<url>')
def search_google_land(url):
    print("PASSED A /URL URL IS: " + url)    
    if url == "search":
        print("SEARCHING ON GOOGLE")
        url = 'https://www.google.com/' + url
        r = requests.get(url)
        rr = Response(response=r.content, status=r.status_code)
        rr.headers["Content-Type"] = r.headers['Content-Type']
        return rr
    return ""

if __name__ == '__main__':
    app.run()
