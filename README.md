# What's this?

Web app showing stops and departures in your vicinity based on data from rejseplanen.dk (http://labs.rejseplanen.dk/api)

# How do I use it?

* You can try it at http://flaskplan.sloppy.zone/

* To start a local instance on port 5000 `make run`

* To start a docker container on port 8000 `make docker-run` (use sudo on linux)

# Files

* `Dockerfile`: wrap this app as a docker container using `mod-wsgi`
* `travis.yml` : configuration for `https://travis-ci.org/`
* `website/__init__.py` : The app...
* `website/static`: static resources
* `website/static/underscore.js`: used in fronten code
* `website/static/main.js`: frontend JavaScript
* `website/rejseplanen.py`: interface to the public API of rejseplanen.dk (`http://labs.rejseplanen.dk/api`)
* `website/templates/index.html`: the index page
* `run.py`: starts a local instance
* `cfg/flaskplan.conf`: apache configuration
* `test/test_rejseplanen.py`: test parsing
* `test/test_app.py`: test the backend part of the app
* `test/data/`: test data
* `requirements.txt`: python dependencies
* `flaskplan.wsgi`: wsgi entry point for apache
* `Makefile`: make file
* `flaskplan.json`: deployment definition for sloppy.io
* `LICENSE`: Apache License 2.0
* `README.md`: this readme

# Service Description

The backend implements two REST service calls. The response format is always JSON.
The design goal has been to provide a service that makes the implementation of the
frontend as convenient as possible.

## `/location?lat=<latitude>&lon=<longitude>`

This service call will return the closest stop given the coordinates in WGS 84.

Parameters:
 * lat: the latitude (example: `56.17118730000001`)
 * lon: the longitude (example: `10.197282399999999`)

The response is always a JSON array with one element for each stop.

Response keys:
 * lat/lon: the latitude/longitude of the stop
 * distance: distance from the current position
 * name: the name of the stop
 * id: a unique id used in request to the `/departures` service

Example Response:

~~~
[{
  'lat': 56.170104,
  'distance': '137',
  'lng': 10.19837,
  'id': '751428000',
  'name': 'Aarhus Universitet. Statsbiblioteket. Langelandsg.'
  }, {
  'lat': 56.170994,
  'distance': '184',
  'lng': 10.200249,
  'id': '751406800',
  'name': 'Aarhus Universitet. Statsbiblioteket og Stakladen'
}]
~~~

## `/departures?id=<stopid>`

The service call will return the next departures given a stop id.

Parameters:
 * id: A stop id from a  `/location` call.

Response keys:

* direction: In which direction does route go.
* name: The name of the route.
* time: The departure time.

Example Response:

~~~
[{
  'direction': 'Holme Parkvej',
  'name': 'Bybus 16',
  'time': '18:30'
  }, {
  'direction': 'Holme Parkvej',
  'name': 'Bybus 16',
  'time': '19:30'
}]
~~~