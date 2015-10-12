import binascii
import gpxpy
import gpxpy.gpx
from dateutil.parser import parse
import struct
import argparse
import os

''' 
Parse record byte array and return dictionay containing latitude, longtitude, date and altitude
Based on Robware answer on https://www.reddit.com/r/ukbike/comments/29i7nt/did_anyone_else_get_the_gps_watch_from_the_aldi/

(changed long/lat, numbering starts from 0)

GPS Data (32 bytes):
00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31
-----------------------------------------------------------------------------------------------
  |  |Y |M |D |H |m |S | Long      | Lat       |Alt  | Head|Speed|Dist |HR|  |  |  |  |  |  |

'''
def parse_record(bytes):
	res = {}
	#timestamp 3->8
	res['date'] = parse("20"+ "-".join(map(lambda b: str(ord(b)).zfill(2),bytes[2:5]))+"T"+":".join(map(lambda b: str(ord(b)).zfill(2),bytes[5:8]))+"Z")	
	#longtitude	8->11
	lon_bytes = bytes[8:12][::-1] #reverse bytes
	res['lon'] = str(struct.unpack('>i', binascii.hexlify(bytearray(lon_bytes)).decode('hex'))[0]/10000000.0)
	#latitude 12->15
	lat_bytes =  bytes[12:16][::-1]	#reverse bytes	
	res['lat'] = str(struct.unpack('>i', binascii.hexlify(bytearray(lat_bytes)).decode('hex'))[0]/10000000.0)	
	#altitude
	alt_bytes =  bytes[16:18][::-1] #reverse bytes
	res['alt'] = str(int(binascii.hexlify(bytearray(alt_bytes)),16))
	return res


'''
Parse tkl file
Based on Robware answer on https://www.reddit.com/r/ukbike/comments/29i7nt/did_anyone_else_get_the_gps_watch_from_the_aldi/

Header (256 bytes?):
...
Lap data (16 bytes?):
...
GPS Data (32 bytes):
...

GPS Data starts at 256+16=272 byte
'''
def read_file(filename):
	f = open(filename, "rb")
	try:
	    f.seek(272) #skip header + lap data
	    #each record is 32 bytes
	    bytes = f.read(32) 
	    ar = []
	    while bytes != "":
	        dct = parse_record(bytes)
	        ar.append(dct)
	        bytes = f.read(32)
	    return ar	        
	finally:
	    f.close()

'''
Create gpx file from extracted gps data
'''
def create_gpx(records):
	gpx = gpxpy.gpx.GPX()

	# Create first track in our GPX:
	gpx_track = gpxpy.gpx.GPXTrack()
	gpx.tracks.append(gpx_track)

	# Create first segment in our GPX track:
	gpx_segment = gpxpy.gpx.GPXTrackSegment()
	gpx_track.segments.append(gpx_segment)

	# Create points:
	for record in records:
		gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(record['lat'], record['lon'], elevation=record['alt'],time=record['date']))

	# You can add routes and waypoints, too...
	return gpx.to_xml()


#simple app to convert input files
argparser = argparse.ArgumentParser('tkl-parser.py')
argparser.add_argument('source',help="File or directory to read from")

source_files = []

if os.path.isdir(argparser.parse_args().source):
	source_files = map(lambda file: os.path.join(argparser.parse_args().source, file),filter(lambda file: file.endswith(".tkl"), os.listdir(argparser.parse_args().source)))
else:
	source_files.append(argparser.parse_args().source)

for file in source_files:
	out_file = ''
	try:
		print "Converting:" + file,
		out_file = open(file+".gpx","w")
		out_file.write(create_gpx(read_file(file)))
		print "Done" 
	except:	
		print "Failed"
	finally:
		if out_file:	
			out_file.close()
		
	




