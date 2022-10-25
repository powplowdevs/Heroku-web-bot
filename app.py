#IMPORTS
import os
import requests
from lxml import html

from flask import Flask
from flask import Response
from flask import request
from flask import request as re

#APP
app = Flask(__name__)


#MAIN ROUTE
@app.route('/')
def home():
    usage = 'Enter a valid URL into the serach bar after this URL such as -> /h/google.com'
    return usage

#HANDLE BASIC URLS
@app.route('/h/<url>')
def root(url): 
    try:
        #GRAB SITE HTML
        r = requests.get(url)
        #EDIT SOURCES IN HTML TO HAVE "https://www.google.com/" BEFORE THEM
        new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')
        
        #DISPLAY URL
        print("Fecthing: " + str(r.url))

        #CREATE RETRUN OBJECT
        rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
        rr.headers["Content-Type"] = r.headers['Content-Type']

        #HANDLE 404
        if str(r.status_code) == "404":
            #TRY URL BUT NOW WITH "https://google.com/" INFRONT
            url = "https://google.com/" + url

            #DISPLAY ERROR URL
            print("Error fetching base url, new url is: " + url)
            print("url: ", url)

            #GRAB SITE HTML
            r = requests.get(url)
            #EDIT SOURCES IN HTML TO HAVE "https://www.google.com/" BEFORE THEM
            new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')

            #CREATE RETRUN OBJECT
            rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
            rr.headers["Content-Type"] = r.headers['Content-Type']

            #RETURN
            return rr

    #HANDLE 404
    except:
        #DISPLAY NEW URL
        print("Error fetching [" + url + "]\nFull url: https://" + url)

        #EDIT URL TO HAVE https:// BEFORE
        url = "https://" + url

        #GRAB SITE HTML
        r = requests.get(url)
        #EDIT SOURCES IN HTML TO HAVE "https://www.google.com/" BEFORE THEM
        new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')
        
        #CREATE RETRUN OBJECT
        rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
        rr.headers["Content-Type"] = r.headers['Content-Type']

        #RETURN
        return rr


@app.route('/<u>', methods=['GET'])
def search(u):
    #GRAB ALL ARGS FOR SITE
    args = request.args
    #GRAB URL FOR SITE
    name = args.get("q")

    try:
        #HANDLE GOOGLE SEARCH
        if len(name) >= 4 and name[0:5] != "https" or len(name) < 4:
            #DEFINE URL WITH THE URL WE WANT TO ACCESS
            url = "https://www.google.com/search?q=" + args.get("q")
            print("SEARCHING: ", url)
            
            #GRAB SITE HTML
            r = requests.get(url)
            #EDIT SOURCES IN HTML TO HAVE "https://www.google.com/" BEFORE THEM
            new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')
            
            #CREATE RETRUN OBJECT
            rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
            rr.headers["Content-Type"] = r.headers['Content-Type']

        #HANDLE OPEN SITE
        elif len(name) >= 4 and name[0:5] == "https":
            url = args.get("q")
            print("SITE URL: ",)

            r = requests.get(url)
            #new = (r.content).decode("windows-1252").replace('src="','src="' + str(r.url))
                
            print("Fecthing: " + str(r.url))

            rr = Response(response=r.content, status=r.status_code)
            print("CONTENT: ", r.content)
            print("\n")
            print("HEADDERS: ", r.headers)
            rr.headers["Content-Type"] = r.headers['Content-Type']

        #HANDLE OTHERS
        else:
            print("OTHER")
            url = "https://" + args.get("q")

            r = requests.get(url)
            new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')

            print("Fecthing: " + str(r.url))

            rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
            rr.headers["Content-Type"] = r.headers['Content-Type']
    
    #IF SITE 404's        
    except:
        rr = ""

    return rr

if __name__ == '__main__':
    app.run()
