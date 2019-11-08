from media import *

class VideoInfo(Media):
	def __init__(self, link, html):
		super().__init__(link, html)
		m = re.search('width\":(.+?),', html)
		self.width = m.group(1)
		m = re.search('height\":(.+?),', html)
		self.height = m.group(1)
		m = re.search('fps\":(.+?),', html)
		self.fps = m.group(1)
		m = re.search('qualityLabel\":\"(.+?)\",', html)
		self.qualityLabel = m.group(1)

	def __str__(self):
		return super().__str__()+\
		'width: '+self.width+'\nheight: '+self.height+'\nfps: '+self.fps+\
		'\nqualityLabel: '+self.qualityLabel+'\n';
