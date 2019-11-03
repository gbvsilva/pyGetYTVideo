from media import *

class AudioJSON(Media):
	"""docstring for AudioJSON"""
	def __init__(self, html):
		super().__init__(html)
		m = re.search('audioQuality\":\"(.+?)\",', html)
		self.audioQuality = m.group(1)
		m = re.search('audioSampleRate\":\"(.+?)\",', html)
		self.audioSampleRate = m.group(1)
		m = re.search('audioChannels\":(.+?),', html)
		self.audioChannels = m.group(1)

	def __str__(self):
		return super().__str__()+\
		f'\naudioQuality: {self.audioQuality}\naudioSampleRate: '+\
		f'{self.audioSampleRate}\naudioChannels: {self.audioChannels}'