#!/usr/bin/env python
import sys, urllib2, json

if len(sys.argv) < 2:
				sys.exit("Usage: getvod.py <video-id>")

url = "http://api.justin.tv/api/broadcast/by_archive/%s.json" % sys.argv[1]
print "Retrieving VOD list from %s" % url
try:
				response = urllib2.urlopen(url)
				data = json.loads(response.read())
except:
				sys.exit("Looks like something went wrong - perhaps you entered an incorrect Video ID?")

for video_part in data:
				flv = video_part["video_file_url"]
				file_name = flv.split('/')[-1]
				u = urllib2.urlopen(flv)
				f = open(file_name, 'wb')
				block_sz = 8192
				file_size_dl = 0
				meta = u.info()
				file_size = int(meta.getheaders("Content-Length")[0])
				print "Downloading: %s Bytes: %s" % (file_name, file_size)
				while True:
								buffer = u.read(block_sz)
								if not buffer:
												break

								file_size_dl += len(buffer)
								f.write(buffer)
								status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
								status = status + chr(8)*(len(status)+1)
								sys.stdout.write("\r%s"  % status)
								sys.stdout.flush()
				f.close()
