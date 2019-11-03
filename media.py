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
		
		self.initRange = None
		m = re.search('initRange\":{\"start\":\"(.+?)\",\"end\":\"(.+?)\"},', html)
		if m:
			self.initRange = {"start": m.group(1), "end": m.group(2)}
		
		self.indexRange = None
		m = re.search('indexRange\":{\"start\":\"(.+?)\",\"end\":\"(.+?)\"},', html)
		if m:
			self.indexRange = {"start": m.group(1), "end": m.group(2)}
		
		m = re.search('lastModified\":\"(.+?)\",', html)
		self.lastModified = m.group(1)

		self.contentLength = None
		m = re.search('contentLength\":\"(.+?)\",', html)
		if m:
			self.contentLength = m.group(1)

		m = re.search('quality\":\"(.+?)\",', html)
		self.quality = m.group(1)
		m = re.search('projectionType\":\"(.+?)\"', html)
		self.projectionType = m.group(1)

		self.averageBitrate = None
		m = re.search('averageBitrate\":(.+?),', html)
		if m:
			self.averageBitrate = m.group(1)
		self.approxDurationMs = None
		m = re.search('approxDurationMs\":\"(.+?)\"', html)
		if m:
			self.approxDurationMs = m.group(1)
		
		self.url = ''
		self.cipher = ''
		m = re.search('cipher\":\"(.+?)\"', html)
		if m:
			self.cipher = m.group(1)
			self.url = None
		else:
			self.cipher = None
			self.url = re.search('url\":\"(.+?)\"', html).group(1)

	def genURL(self):
		if self.cipher:
			parsed_cipher = urllib.parse.unquote(self.cipher)
			if parsed_cipher.index('s=') < parsed_cipher.index('url='):
				url = re.search('url=(.+)', parsed_cipher).group(1)
				m = re.search('s=(.+?)LAu0026', parsed_cipher)
			else:
				url = re.search('url=(.+?)u0026', parsed_cipher).group(1)
				m = re.search('u0026s=(.+LA?)LA', parsed_cipher)
			
			sig = list(m.group(1))
			sig.reverse()
			sig = ''.join(sig)
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
			self.url = url+'&sig='+sig
		else:
			self.url = self.url.replace('u0026', '&')

	def __str__(self):
		out = f'itag: {self.itag}\nmimeType: {self.mimeType}\nbitrate: {self.bitrate}\n'+\
		f'lastModified: {self.lastModified}\nquality: {self.quality}\n'+\
		f'projectionType: {self.projectionType}\n'
		out += 'initRange: {}'.format(str(self.initRange)+'\n' if self.initRange else 'None\n')
		out += 'indexRange: {}'.format(str(self.indexRange)+'\n' if self.indexRange else 'None\n')
		out += 'contentLength: {}'.format(self.contentLength+'\n' if self.contentLength else 'None\n')
		out += 'averageBitrate: {}'.format(self.averageBitrate+'\n' if self.averageBitrate else 'None\n')
		out += 'approxDurationMs: {}'.format(self.approxDurationMs+'\n' if self.approxDurationMs else 'None\n')
		out += 'cipher: {}'.format(self.cipher+'\n' if self.cipher else 'None\n')
		return out