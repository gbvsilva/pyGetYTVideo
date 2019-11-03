import urllib.request
import re

class JSON:
	def __init__(self, html):
		m = re.search('itag\":(.+?),', html)
		self.itag = m.group(1)
		m = re.search('mimeType\":\"(.+?)\",', html)
		self.mimeType = m.group(1)
		m = re.search('bitrate\":(.+?),', html)
		self.bitrate = m.group(1)
		m = re.search('width\":(.+?),', html)
		self.width = m.group(1)
		m = re.search('height\":(.+?),', html)
		self.height = m.group(1)
		m = re.search('initRange\":{\"start\":\"(.+?)\",\"end\":\"(.+?)\"},', html)
		self.initRange = {"start": m.group(1), "end": m.group(2)}
		#print(self.initRange)
		m = re.search('indexRange\":{\"start\":\"(.+?)\",\"end\":\"(.+?)\"},', html)
		self.indexRange = {"start": m.group(1), "end": m.group(2)}
		m = re.search('lastModified\":\"(.+?)\",', html)
		self.lastModified = m.group(1)
		m = re.search('contentLength\":\"(.+?)\",', html)
		self.contentLength = m.group(1)
		m = re.search('quality\":\"(.+?)\",', html)
		self.quality = m.group(1)
		m = re.search('fps\":(.+?),', html)
		self.fps = m.group(1)
		m = re.search('qualityLabel\":\"(.+?)\",', html)
		self.qualityLabel = m.group(1)
		m = re.search('projectionType\":\"(.+?)\"', html)
		self.projectionType = m.group(1)
		m = re.search('averageBitrate\":(.+?),', html)
		self.averageBitrate = m.group(1)
		m = re.search('approxDurationMs\":\"(.+?)\",', html)
		self.approxDurationMs = m.group(1)
		m = re.search('cipher\":\"(.+?)\"}', html)
		self.cipher = m.group(1)

	def __str__(self):
		return f'itag: {self.itag}\nmimeType: {self.mimeType}\nbitrate: {self.bitrate}\n'+\
		f'width: {self.width}\nheight: {self.height}\ninitRange: {self.initRange}\n'+\
		f'indexRange: {self.indexRange}\nlastModified: {self.lastModified}\ncontentLength: '+\
		f'{self.contentLength}\nquality: {self.quality}\nfps: {self.fps}\nqualityLabel: '+\
		f'{self.qualityLabel}\nprojectionType: {self.projectionType}\naverageBitrate: '+\
		f'{self.averageBitrate}\napproxDurationMs: {self.approxDurationMs}\ncipher: {self.cipher}'
		
	
url = input()

with urllib.request.urlopen(url) as response:
	html = response.read()
	i = html.index('{\\\"itag\\\":243'.encode())
	j = html[i:].index(',{\\\"itag\\\":'.encode())
	json = JSON(html[i:i+j].decode().translate({ord('\\'): None}))
	print(json.cipher)
