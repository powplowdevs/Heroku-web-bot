#IMPORTS
import os
import requests
from lxml import html

from flask import Flask, render_template
from flask import jsonify
from flask import Response
from flask import request
from flask import request as re
from flask_cors import CORS, cross_origin
import os

#APP
app = Flask(__name__)
CORS(app, support_credentials=True)

#vars
current_domain = ""
site_url = "https://py-pro-proxy.herokuapp.com/"
use_prox = False

proxies = {
"http": os.environ['QUOTAGUARDSTATIC_URL'],
"https": os.environ['QUOTAGUARDSTATIC_URL']
}

#MAIN ROUTE
@app.route('/')
def home():
    return "home"

#HANDLE BASIC URLS
@app.route('/h/<url>')
def root(url): 
    global current_domain
    try:
        #GRAB SITE HTML
        r = requests.get(url)
        current_domain = url
        
        #EDIT SOURCES IN HTML TO HAVE "https://www.google.com/" BEFORE THEM
        new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')
        
        #DISPLAY URL
        print("Fecthing: " + str(r.url))

        #CREATE RETRUN OBJECT
        rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
        rr.headers["Content-Type"] = r.headers['Content-Type']
        rr.headers["Access-Control-Request-Method"] = "post"
        rr.headers["Access-Control-Request-Headers"] = "X-Requested-With"
        
        #HANDLE 404
        if str(r.status_code) == "404":
            #TRY URL BUT NOW WITH "https://google.com/" INFRONT
            url = "https://google.com/" + url
            current_domain = url

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
            rr.headers["Access-Control-Request-Method"] = "post"
            rr.headers["Access-Control-Request-Headers"] = "X-Requested-With"
            
                   
            #RETURN
            return rr

    #HANDLE 404
    except:
        #DISPLAY NEW URL
        print("Error fetching [" + url + "]\nFull url: https://" + url)

        #EDIT URL TO HAVE https:// BEFORE
        url = "https://" + url
        current_domain = url

        #GRAB SITE HTML
        r = requests.get(url)
        #EDIT SOURCES IN HTML TO HAVE "https://www.google.com/" BEFORE THEM
        new = (r.content).decode("windows-1252").replace('src="','src="https://www.google.com/')
        
        #CREATE RETRUN OBJECT
        rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
        rr.headers["Content-Type"] = r.headers['Content-Type']
        rr.headers["Access-Control-Request-Method"] = "post"
        rr.headers["Access-Control-Request-Headers"] = "X-Requested-With"
            
        #RETURN
        return rr


@app.route('/<u>', methods=['GET'])
def search(u):
    global current_domain

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
            rr.headers["Access-Control-Request-Method"] = "post"
            rr.headers["Access-Control-Request-Headers"] = "X-Requested-With"

        #HANDLE OPEN SITE
        elif len(name) >= 4 and name[0:5] == "https":
            url = args.get("q")
            temp_url = url.replace("https://","")
            current_domain =  "https://" + temp_url[:temp_url.index("/")+1]
        
            print("SITE URL: ", url)
            if use_prox:
                print("useing proxy")
                r = requests.get(url, proxies=proxies)
            else:
                r = requests.get(url)

            new = (r.content).decode("windows-1252").replace('href="','href="' + site_url + "url?q=" + current_domain)
            new = (r.content).decode("windows-1252").replace('href="/','href="' + site_url + "url?q=" + current_domain)

            rr = Response(response=new, status=r.status_code)
            r.headers["X-Content-Type-Options"] = "nosniff"
            rr.headers["Content-Type"] = r.headers['Content-Type']
            rr.headers["Access-Control-Request-Method"] = "post"
            rr.headers["Access-Control-Request-Headers"] = "X-Requested-With"
            
        #HANDLE OTHERS
        else:
            print("OTHER")
            url = "https://" + args.get("q")

            if use_prox:
                print("useing proxy other")
                r = requests.get(url, proxies=proxies)
            else:
                r = requests.get(url)
                
            new = (r.content).decode("windows-1252").replace('href="','href="' + site_url + "url?q=" + current_domain)
            new = (r.content).decode("windows-1252").replace('href="/','href="' + site_url + "url?q=" + current_domain)

            print("Fecthing other: " + str(r.url))

            rr = Response(response=bytes(new, encoding="windows-1252"), status=r.status_code)
            rr.headers["Content-Type"] = r.headers['Content-Type']
            rr.headers["Access-Control-Request-Method"] = "post"
            rr.headers["Access-Control-Request-Headers"] = "X-Requested-With"
    
    #IF SITE 404's        
    except:
        rr = ""

    return rr

@app.errorhandler(404) 
def invalid_route(e): 
    if current_domain != "https://google.com ":
        url = current_domain + (request.url).replace(site_url, "")
    else:
        url = current_domain + (request.url).replace(site_url, "/")
        
    print("SITE URL 404: ", url)

    r = requests.get(url)

    print("Fecthing 404: " + str(r.url))
    
    new = (r.content).decode("windows-1252").replace('href="','href="' + site_url + "url?q=" + current_domain)
    new = (r.content).decode("windows-1252").replace('href="/','href="' + site_url + "url?q=" + current_domain)

    rr = Response(response=new, status=r.status_code)
    r.headers["X-Content-Type-Options"] = "nosniff"
    rr.headers["Content-Type"] = r.headers['Content-Type']
    rr.headers["Access-Control-Request-Method"] = "post"
    rr.headers["Access-Control-Request-Headers"] = "X-Requested-With"

    return rr


if __name__ == '__main__':
    app.run()
