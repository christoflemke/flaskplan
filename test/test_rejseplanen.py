# -*- coding: utf-8 -*-

import sys
import os
import unittest
import json

sys.path.insert(0, os.path.abspath('..'))
from website.rejseplanen import convertStops,convertDepartures

class TestRejseplanen(unittest.TestCase):
    'test conversion of data given example data'
    
    def testConvertStops(self):
        with open('data/stopsNearby.json','r') as f:
            j=json.load(f,'UTF-8')
            stops = convertStops(j);
            self.assertEqual(stops[0], {
                u"name": u"Halmstadgade v. Skøjtehallen (Aarhus)",
                u"lng": 10.188778,
                u"lat": 56.181871,
                u"id":u"751419500",
                u"distance":u"115"
            })

    def testConvertDepartures(self):
        with open('data/departures.json','r') as f:
            j=json.load(f,'UTF-8')
            departures = convertDepartures(j)
            
            self.assertEqual(departures[0], {
                'name' : 'Bybus 1A',
                'time' : '21:56',
                'direction' : 'Trige via AUH Skejby'
            })
        
if __name__ == '__main__':
    unittest.main()
