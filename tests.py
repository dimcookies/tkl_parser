import unittest
import tkl_parser
from datetime import date,datetime
import xml.etree.ElementTree

class TestStringMethods(unittest.TestCase):
	def test_create_gpx(self):
		test_data = [
			{'lat':"1",'lon':"2",'alt':'3','date':date(2015, 10, 26)},
			{'lat':"4",'lon':"5",'alt':'6','date':date(2016, 11, 27)}
		]
		res = tkl_parser.create_gpx(test_data)
		gpx = xml.etree.ElementTree.fromstring(res)
		self.assertEquals(gpx.tag.endswith("gpx"), True)
		trk = gpx.find("{http://www.topografix.com/GPX/1/0}trk")
		trkseg = trk.find("{http://www.topografix.com/GPX/1/0}trkseg")
		points = trkseg.findall("{http://www.topografix.com/GPX/1/0}trkpt")
		self.assertEqual(test_data[0], parse_trkpt(points[0]))
		self.assertEqual(test_data[1], parse_trkpt(points[1]))

	def test_parse_record(self):
		records = [
			0,55,14,7,2,17,35,43,177,192,195,254,242,8,188,31,
			203,0,25,1,154,0,33,0,106,170,170,170,170,170,170,170
		]
		records = map(lambda x:chr(x), records)
		res = tkl_parser.parse_record(records)
		self.assertEquals(res['lat'],"53.2416754")
		self.assertEquals(res['lon'],"-2.0725583")
		self.assertEquals(res['alt'],"203")
		self.assertEquals(res['date'].date(),datetime.strptime("2014-07-02T17:35:43Z",'%Y-%m-%dT%H:%M:%SZ').date()) 


def parse_trkpt(point):
	res = point.attrib
	res['alt'] = point.find("{http://www.topografix.com/GPX/1/0}ele").text
	res['date'] = datetime.strptime(point.find("{http://www.topografix.com/GPX/1/0}time").text,'%Y-%m-%dT%H:%M:%SZ').date()
	return res
	

if __name__ == '__main__':
    unittest.main()
