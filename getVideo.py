import urllib.request
from media import *
	
link = input()
while True:
	with urllib.request.urlopen(link) as response:
		html = response.read()
		i = html.index('{\\\"itag\\\":18'.encode())
		j = html[i:].index('}]'.encode())
		video = Media(link, html[i:i+j].decode().translate({ord('\\'): None}))
		
		print("==== Video Info ====")
		print(video)
		
		video.genURL()
		if video.url:
			print('Video_url: {}'.format(video.url if video.url else 'None'))
			break
