import urllib
import json

class RejseplanClient:
    'Access to the rejseplanen.dk api'
    
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def execute(self,path,params):
        url = self.baseurl+"/"+path+"?%s" % params;
        f = urllib.urlopen(url)
        response = json.loads(f.read());
        return response;
        
    def stopsNearby(self,coordX, coordY, maxRadius = 500, maxNumbers = 30):
        'retrieve the stops closest to the location'
        'the coordinates are given as floats in the WSG 84 system'
        
        params = urllib.urlencode({
            'coordX': int(coordX*1000000),
            'coordY': int(coordY*1000000),
            'maxRadius' : maxRadius,
            'maxNumbers' : maxNumbers,
            'format' : 'json'})
        return self.execute('stopsNearby',params)

    def departureBoard(stationId):
        params = urllib.urlencode({'id' : stationId, 'format' : 'json'})
        return self.execute('departureBoard', params);


def convertDepartures(json):
    return [{
        'name' : r['name'],
        'time' : r['time'],
        'direction' : r['direction']
    } for r in json['DepartureBoard']['Departure']]

def convertStops(json):
    return [{
        'id' : location['id'],
        'name' : location['name'],
        'lat': float(location['y'])/1000000.0,
        'lng': float(location['x'])/1000000.0,
        'distance' : location['distance']
    } for location in json['LocationList']['StopLocation']];
