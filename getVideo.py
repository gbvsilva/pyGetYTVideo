# python3
import urllib.request
from subprocess import Popen, PIPE
from media import *
	
link = input()
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

while True:
	req = urllib.request.Request(link, data=None, headers=headers)
	with urllib.request.urlopen(req) as response:
		html = response.read()
		i = html.index('{\\\"itag\\\":18'.encode())
		j = html[i:].index('}]'.encode())
		
		video = Media(link, html[i:i+j].decode().translate({ord('\\'): None}))
		
		print("==== Video Info ====")
		print(video)
		
		video.genURL()
		if video.url:
			print('Video_url: {}'.format(video.url if video.url else 'None'))
			open_video = input('\nOpen video? (Y/N) ')
			if open_video.lower() == 'y':
				p1 = Popen(['which', 'x-www-browser'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
				browser = p1.stdout.read()
				browser = browser[:-1] # removing new line
				p2 = Popen([browser, video.url], stdout=PIPE, stderr=PIPE, stdin=PIPE)
			break
