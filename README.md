# tkl_parser
Converter for tkl files to gpx

A python application to convert tkl files as stored by "GPS Master" software (name may be different based on the company). Using GPS Master you can export a track to gpx so this is useful for bulk converting of existing files.

The implementation has been based on comments of the user Robware on the following reddit thread 

https://www.reddit.com/r/ukbike/comments/29i7nt/did_anyone_else_get_the_gps_watch_from_the_aldi/

For gpx file creating, gpxpy library is used

https://github.com/tkrajina/gpxpy

#Other info:
In case you need a replacement of GPS Master or a tool for linux to access directly your watch you can check the following

https://github.com/mru00/crane_gps_watch

There is a similar tool in java for convertion (produced with reverse engineering of the original program )

https://github.com/dobson156/Tkl2Gpx

For Windows users you can check the following post for a tool that bulk converts/exports routes from GPS Master
http://www.mcdruid.co.uk/content/bulk-export-gps-data-from-ultrasport-navrun-500-watch

