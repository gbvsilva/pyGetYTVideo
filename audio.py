from media import *

class AudioInfo(Media):
	"""docstring for AudioInfo"""
	def __init__(self, link, html):
		super().__init__(link, html)
		m = re.search('audioQuality\":\"(.+?)\",', html)
		self.audioQuality = m.group(1)
		m = re.search('audioSampleRate\":\"(.+?)\",', html)
		self.audioSampleRate = m.group(1)
		m = re.search('audioChannels\":(.+?)', html)
		self.audioChannels = m.group(1)

	def __str__(self):
		return super().__str__()+\
		f'audioQuality: {self.audioQuality}\naudioSampleRate: '+\
		f'{self.audioSampleRate}\naudioChannels: {self.audioChannels}'