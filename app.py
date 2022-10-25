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
from flask import request
from flask import request as re

app = Flask(__name__)


@app.route('/')
def home():
    print("HOME")
    usage = 'Enter a valid URL into the serach bar after this URL such as -> /https/www.google.com'
    return usage

#BASIC URLS
@app.route('/h/<url>')
def root(url): 
    try:
        if url != "search":
            url = url

            r = requests.get(url)
            new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')

            print("Fecthing: " + str(r.url))

            rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
            rr.headers["Content-Type"] = r.headers['Content-Type']

            #print(r.content, "main")

            print("RESPONE CODE" + str(r.status_code) + "\n")

            if str(r.status_code) == "404":
                url = "https://google.com/" + url

                print("Error fetching base url, new url is: " + url)
                print("url: ", url)

                r = requests.get(url)
                new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')

                print("Fecthing: " + str(r.url))

                rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
                rr.headers["Content-Type"] = r.headers['Content-Type']

                #print(r.content, "404")

                return rr

            return rr
    except:
        print("Error fetching [" + url + "]\nFull url: https://" + url)

        url = "https://" + url

        r = requests.get(url)
        new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')

        print("rurl", r.url)
        print("RESPONE CODE" + str(r.status_code))

        rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
        rr.headers["Content-Type"] = r.headers['Content-Type']

        #print(bytes(new, encoding="windows-1252"), "ERROR")

        return rr

def page_not_found(e):
  return "404"


@app.route('/<u>', methods=['GET'])
def search(u):
    args = request.args
    print("ARGS: ",args.get("q"),"\n")
    name = args.get("q")
    print(args)
    print(name)
    print("ARGS FOR NAME: ", len(name), name[0:4])
    try:
        if len(name) >= 4 and name[0:5] != "https" or len(name) < 4:
            print("SEARCHING")
            url = "https://www.google.com/search?q=" + args.get("q")

            r = requests.get(url)
            new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')

            print("Fecthing: " + str(r.url))

            rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
            rr.headers["Content-Type"] = r.headers['Content-Type']
        elif len(name) >= 4 and name[0:5] == "https":
            print("SITE URL")
            url = args.get("q")

            print("URLS: ",url)
            r = requests.get(url)
            #new = (r.content).decode("windows-1252").replace('src="','src="' + str(r.url))

            print("Fecthing: " + str(r.url))

            rr = Response(response=r.content, status=r.status_code)
            rr.headers["Content-Type"] = r.headers['Content-Type']
        else:
            print("OTHER")
            url = "https://" + args.get("q")

            r = requests.get(url)
            new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')

            print("Fecthing: " + str(r.url))

            rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
            rr.headers["Content-Type"] = r.headers['Content-Type']
    except:
        rr = ""

    return rr

# #SEARCH GOOGLE
# @app.route('/<url>')
# def search_google_land(url):
#     print("PASSED A /URL URL IS: " + url)    
#     if url == "search":
#         print("SEARCHING ON GOOGLE")
#         url = 'https://www.google.com/' + url
#         r = requests.get(url)
#         rr = Response(response=r.content, status=r.status_code)
#         rr.headers["Content-Type"] = r.headers['Content-Type']
#         return rr
#     return ""

import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    app.run()
