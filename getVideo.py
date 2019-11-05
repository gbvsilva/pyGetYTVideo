import urllib.request
#from audio import AudioInfo
#from video import VideoInfo
from media import *
	
url = input()

with urllib.request.urlopen(url) as response:
	html = response.read()
	i = html.index('{\\\"itag\\\":18'.encode())
	j = html[i:].index('}]'.encode())
	video = Media(html[i:i+j].decode().translate({ord('\\'): None}))
	
	# i = html.index('{\\\"itag\\\":140'.encode())
	# j = html[i:].index('}]}'.encode())+1
	# audio_info = AudioInfo(html[i:i+j].decode().translate({ord('\\'): None}))

	print("==== Video Info ====")
	print(video)
	# print("\n==== Audio Info ====")
	# print(audio_info)
	
	video.genURL()
	print('Video_url: {}'.format(video.url if video.url else 'None'))
	# audio_info.genURL()
	# print('Audio_url: '+audio_info.url)
