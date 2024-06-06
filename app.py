import os
import requests
from flask import Flask, jsonify, Response, request
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, support_credentials=True)

# CORS Proxy URL
corbsProxUrl = "https://api.allorigins.win/raw?url="

# Vars
currentDomain = ""
siteUrl = "https://py-pro-proxy.herokuapp.com/"  # or "http://127.0.0.1:5000/"
useProx = False
useCorbsProx = False

#Proxies example (commented out)
# proxies = {
#     "http": os.environ['QUOTAGUARDSTATIC_URL'],
#     "https": os.environ['QUOTAGUARDSTATIC_URL']
# }

# Function to modify URLs in HTML content
def modifyUrls(content, base_url):
    try:
        try:
            content = content.decode("windows-1252")
        except UnicodeDecodeError:
            content = content.decode("utf-8")
        
        # Parse HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Modify href attributes
        for link in soup.find_all('a', href=True):
            if link['href'].startswith(base_url):
                link['href'] = link['href'].replace(base_url, '')

        # Modify src attributes
        for img in soup.find_all('img', src=True):
            if img['src'].startswith(base_url):
                img['src'] = img['src'].replace(base_url, '')

        return str(soup)
    except Exception as e:
        print(f"Error modifying URLs: {e}")
        return Response("Error processing the HTML content", status=500)

def trimUrl(url):
    parts = url.split('/')
    #Check if there are more than 3 parts (to avoid index errors)
    if len(parts) > 3:
        trimmedUrl = '/'.join(parts[:3]) + '/'
    else:
        trimmedUrl = url
    return trimmedUrl

@app.route('/')
def home():
    return "Home page, add /h/google.com or /h/https://google.com to the end of the link above to open google."

@app.route('/h/<path:url>')
@cross_origin(supports_credentials=True)
def root(url):
    global currentDomain
    try:
        fullUrl = f"https://{url}" if not url.startswith('http') else url
        fullUrl = trimUrl(fullUrl)
        print(f"Fetching: {fullUrl}")

        r = requests.get(fullUrl)
        currentDomain = fullUrl

        content = r.content
        modifiedContent = modifyUrls(content, siteUrl + "h/")
        response = Response(response=modifiedContent, status=r.status_code)
        response.headers["Content-Type"] = r.headers['Content-Type']
        response.headers["Access-Control-Request-Method"] = "post"
        response.headers["Access-Control-Request-Headers"] = "X-Requested-With"

        return response
    
    except Exception as e:
        try:
            fullUrl = f"https://{url}" if not url.startswith('http') else url
            fullUrl = trimUrl(fullUrl)
            print(f"2nd pass. Fetching: {fullUrl}")

            r = requests.get(fullUrl)
            currentDomain = fullUrl

            content = r.content
            modifiedContent = modifyUrls(content, siteUrl + "h/")
            response = Response(response=modifiedContent, status=r.status_code)
            response.headers["Content-Type"] = r.headers['Content-Type']
            response.headers["Access-Control-Request-Method"] = "post"
            response.headers["Access-Control-Request-Headers"] = "X-Requested-With"

            return response
        except Exception as e:
            print(f"Error fetching [{url}]: {str(e)}")
            return Response("Error fetching the requested URL", status=500)

@app.route('/<u>', methods=['GET'])
@cross_origin(supports_credentials=True)
def search(u):
    global currentDomain
    args = request.args
    query = args.get("q")

    try:
        if query and (len(query) < 4 or not query.startswith("https")):
            url = f"https://www.google.com/search?q={query}"
            print(f"Searching: {url}")
        else:
            url = query

        r = requests.get(url)
        content = r.content
        modifiedContent = modifyUrls(content, siteUrl + "h/")
        response = Response(response=modifiedContent, status=r.status_code)
        response.headers["Content-Type"] = r.headers['Content-Type']
        response.headers["Access-Control-Request-Method"] = "post"
        response.headers["Access-Control-Request-Headers"] = "X-Requested-With"

        return response

    except Exception as e:
        print(f"Error: {str(e)}")
        return Response("Error processing the request", status=500)

@app.errorhandler(404)
def invalidRoute(e):
    global currentDomain
    if(currentDomain[len(currentDomain)-1] != "/"):
        currentDomain = currentDomain + "/"
    currentDomain = currentDomain.replace("https://", "").replace("http://", "")

    try:
        if currentDomain:
            print("\n\n[!+!+!] First op, curr domain: " + currentDomain + "\n[!+!+!] req url: " + request.url.replace(siteUrl + 'h/', ''))
            url = f'{siteUrl}h/{trimUrl(currentDomain)}{request.url.replace(siteUrl, "")}/'
        else:
            print("\n\n[!+!+!] Second op, curr domain: " + currentDomain + "\n[!+!+!] req url: " + request.url.replace(siteUrl + 'h/', ''))
            url = request.url.replace(siteUrl + "h/", "")

        print(f"[404] New URL is: {url}\n\n")
        r = requests.get(url)
        content = r.content
        modifiedContent = modifyUrls(content, siteUrl + "h/")
        response = Response(response=modifiedContent, status=r.status_code)
        response.headers["Content-Type"] = r.headers['Content-Type']
        response.headers["Access-Control-Request-Method"] = "post"
        response.headers["Access-Control-Request-Headers"] = "X-Requested-With"

        return response

    except Exception as e:
        print(f"Error in handling 404: {str(e)}")
        return Response("Error in handling 404", status=500)

if __name__ == '__main__':
    app.run()
