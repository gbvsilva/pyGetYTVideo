import urllib.request
from media import *
	
link = input()
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
#'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
headers = {'User-Agent': user_agent}

while True:
	#print("while")
	req = urllib.request.Request(link, data=None, headers=headers)
	with urllib.request.urlopen(req) as response:
	#print("request")
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
