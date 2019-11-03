import urllib.request
from audio import AudioInfo
from video import VideoInfo
	
url = input()

with urllib.request.urlopen(url) as response:
	html = response.read()
	i = html.index('{\\\"itag\\\":134'.encode())
	j = html[i:].index(',{\\\"itag\\\":'.encode())
	video_info = VideoInfo(html[i:i+j].decode().translate({ord('\\'): None}))
	
	i = html.index('{\\\"itag\\\":140'.encode())
	j = html[i:].index('}]}'.encode())+1
	#print('AUDIO HTML -> '+str(html[i:i+j]))
	audio_info = AudioInfo(html[i:i+j].decode().translate({ord('\\'): None}))
	print("==== Video Info ====")
	print(video_info)
	print("\n==== Audio Info ====")
	print(audio_info)
	#print('\ncipher size -> '+str(len(video_info.cipher)))
	
	video_info.genURL()
	print('\nVideo_url: '+video_info.url)
	audio_info.genURL()
	print('Audio_url: '+audio_info.url)