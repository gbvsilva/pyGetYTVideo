import urllib.request

class JSON:
	def __init__(self, data):
		self.itag
		self.mimeType
		self.bitrate
		self.width
		self.height
		self.initRange = {}
		self.indexRange = {}
		self.lastModified = 
		self.contentLength
		self.quality
		self.fps
		self.qualityLabel
		self.projectionType = data.index('projectionType:')
		
	
url = input()

with urllib.request.urlopen(url) as response:
	html = response.read()
	i = html.index('{\\\"itag\\\":243'.encode())
	j = html[i:].index(',{\\\"itag\\\":'.encode())
	json = JSON(html[i:i+j].decode().translate({ord('\\'): None}))
	#print(html[i:i+j].decode().translate({ord('\\'): None}))
	print(json)
