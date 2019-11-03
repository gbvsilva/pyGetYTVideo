import urllib.request
from audio import AudioJSON
from video import VideoJSON
	
url = input()

with urllib.request.urlopen(url) as response:
	html = response.read()
	i = html.index('{\\\"itag\\\":243'.encode())
	j = html[i:].index(',{\\\"itag\\\":'.encode())
	video_json = VideoJSON(html[i:i+j].decode().translate({ord('\\'): None}))
	
	i = html.index('{\\\"itag\\\":251'.encode())
	j = html[i:].index(',\\\"playerAds\\\"'.encode())-2
	audio_json = AudioJSON(html[i:i+j].decode().translate({ord('\\'): None}))
	#print(audio_json)
	#print('\ncipher size -> '+str(len(video_json.cipher)))
	
	video_url = video_json.genURL()
	print('Video_url: '+video_url)
	audio_url = audio_json.genURL()
	print('Audio_url: '+audio_url)