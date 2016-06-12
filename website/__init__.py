from flask import Flask, render_template, request
import urllib
import os
from flask import json
from rejseplanen import RejseplanClient, convertStops, convertDepartures

app = Flask(__name__)

baseurl = "http://xmlopen.rejseplanen.dk/bin/rest.exe"
rejseplanClient = RejseplanClient(baseurl)
apikey = 'AIzaSyCyOJLtB3rOMlCrdipSb5G4IWvS5Rwx6DM'
    
@app.route("/")
def hello():
    app.logger.debug('index')
    if apikey:
        return render_template("index.html", apikey = apikey)
    else:
        return render_template("index.html")

@app.route("/location")
def locaiton():
    app.logger.debug('location')
    x = request.args.get('lat')
    y = request.args.get('lon')
    app.logger.debug("got lat: %s, lon: %s",x,y)
    coordX=float(x)
    coordY=float(y)
    response = rejseplanClient.stopsNearby(coordX,coordY);
    app.logger.debug(response)
    converted=convertStops(response);
    app.logger.debug(converted)
    return (json.dumps(converted),200, {
        'Content-Type' : 'application/json'
    })

@app.route("/departures")
def departures():
    app.logger.debug('departures')
    stationId = request.args.get('id');
    app.logger.debug('got id: %s',stationId);
    params = urllib.urlencode({'id' : stationId, 'format' : 'json'})
    url = baseurl+"/departureBoard?%s" % params
    app.logger.debug(url)
    f = urllib.urlopen(url)
    rawResponse = f.read()
    jsonRsp = json.loads(rawResponse);
    app.logger.debug(jsonRsp);
    converted = convertDepartures(jsonRsp);
    app.logger.debug(converted)
    return (json.dumps(converted), 200, {
        'Content-Type' : 'application/json'
    })

if __name__ == "__main__":
    app.run()
