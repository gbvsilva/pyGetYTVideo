import re
import urllib.parse

class Media():
	"""docstring for Media"""
	def __init__(self, html):
		m = re.search('itag\":(.+?),', html)
		self.itag = m.group(1)
		m = re.search('mimeType\":\"(.+?)\",', html)
		self.mimeType = m.group(1)
		m = re.search('bitrate\":(.+?),', html)
		self.bitrate = m.group(1)
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
		m = re.search('projectionType\":\"(.+?)\"', html)
		self.projectionType = m.group(1)
		m = re.search('averageBitrate\":(.+?),', html)
		self.averageBitrate = m.group(1)
		m = re.search('approxDurationMs\":\"(.+?)\",', html)
		self.approxDurationMs = m.group(1)
		m = re.search('cipher\":\"(.+?)\"}', html)
		self.cipher = m.group(1)

	def genURL(self):
		parsed_cipher = urllib.parse.unquote(self.cipher)
		if parsed_cipher.index('s=') < parsed_cipher.index('url='):
			url = re.search('url=(.+)', parsed_cipher).group(1)
			m = re.search('s=(.+?)LAu0026', parsed_cipher)
			#print('OK1')
		else:
			url = re.search('url=(.+?)u0026', parsed_cipher).group(1)
			m = re.search('u0026s=(.+LA?)LA', parsed_cipher)
			#print('OK2')
		sig = list(m.group(1))
		#print('\nACTUAL URL -> '+url)
		#print('reversed_sig -> '+''.join(sig))
		sig.reverse()
		sig = ''.join(sig)
		#print('sig -> '+sig+' (size='+str(len(sig))+')')

		sig = list(sig)
		char1 = sig[-1]
		del sig[-1]
		del sig[-1]
		char2 = sig[-12]
		sig[-12] = char1
		if len(sig) == 100:
			sig[45] = char2
		elif len(sig) == 104:
			sig[sig.index('=')] = char2
		sig = ''.join(sig)
		#print('new sig -> '+sig)
		return url+'&sig='+sig

	def __str__(self):
		return f'itag: {self.itag}\nmimeType: {self.mimeType}\nbitrate: {self.bitrate}\n'+\
		f'initRange: {self.initRange}\nindexRange: {self.indexRange}\nlastModified: '+\
		f'{self.lastModified}\ncontentLength: {self.contentLength}\nquality: {self.quality}\n'+\
		f'projectionType: {self.projectionType}\naverageBitrate: {self.averageBitrate}\n'+\
		f'approxDurationMs: {self.approxDurationMs}\ncipher: {self.cipher}'
