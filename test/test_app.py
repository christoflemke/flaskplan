# -*- coding: utf-8 -*-

import sys
import os
import unittest
import json

sys.path.insert(0, os.path.abspath('..'))
from website import app

class TestApp(unittest.TestCase):
    'test app with rejseplanen api'

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        assert b'<title>Flaskplan</title>' in rv.data

    def test_stops(self):
        rv = self.app.get('/location?lat=56.17118730000001&lon=10.197282399999999')
        app.logger.debug(rv.data)
        jsn = json.loads(rv.data)
        self.assertIsInstance(jsn,list)
        # it would be strange if the request would return less thatn 2 results
        self.assertGreater(len(jsn),1)
        # test the structure of the response
        for location in jsn:
            self.assertIsInstance(location,dict)
            keys=set(location.keys())
            self.assertSetEqual(keys, set(['distance','id','lat','lng','name']))


    def test_departures(self):
        # this id is likely to change in the future...
        rv = self.app.get('departures?id=751465300')
        app.logger.debug(rv.data)
        jsn = json.loads(rv.data)
        self.assertIsInstance(jsn,list)
        # should be more than 2 if the id is still valid
        self.assertGreater(len(jsn),1)
        # test the structure of the response
        for departure in jsn:
            self.assertIsInstance(departure,dict)
            keys=set(departure.keys())
            self.assertSetEqual(keys, set(['name','direction','time']))

        
if __name__ == '__main__':
    unittest.main()
