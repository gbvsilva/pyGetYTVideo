import re
import urllib.parse

class Media():
	"""docstring for Media"""
	def __init__(self, link, html):
		self.urlType = 'mobile' if link.startswith("https://m.youtube") else 'desktop'
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
		
		if self.url == None:
			parsed_cipher = urllib.parse.unquote(self.cipher)
			url = ''
			m = ''
			if parsed_cipher.index('s=') < parsed_cipher.index('url='):
				m = re.search('s=(.+?)u0026', parsed_cipher)
				if parsed_cipher.index('url=') < parsed_cipher.index('sp=sig'):
					url = re.search('url=(.+)u0026', parsed_cipher).group(1)
				else:
					url = re.search('url=(.+)', parsed_cipher).group(1)
			else:
				url = re.search('url=(.+?)u0026', parsed_cipher).group(1)
				if parsed_cipher.index('s=') < parsed_cipher.index('sp=sig'):
					m = re.search('u0026s=(.+?)u0026', parsed_cipher)
				else:
					m = re.search('u0026s=(.+?)', parsed_cipher)
			
			sig = list(m.group(1))
			m = re.search('LgxI2', ''.join(sig))
			if m:
				sig.reverse()
				char1 = sig[36]
				sig[36] = sig[-1]
				sig[-1] = char1
				sig[41] = sig[0]
				del sig[0:3]
				sig[0] = 'A'
			else:
				if sig.index('=') > -1 and sig.index('=') < 100:
					sig[sig.index('=')] = sig[-1]
					sig[-1] = '='
					del sig[0]
			self.url = url+'&sig='+''.join(sig)
		else:
			self.url = self.url.replace('u0026', '&')

	def __str__(self):
		out = 'itag: '+self.itag+'\nmimeType: '+self.mimeType+'\nbitrate: '+self.bitrate+\
		'\nlastModified: '+self.lastModified+'\nquality: '+self.quality+\
		'\nprojectionType: '+self.projectionType+'\n'
		out += 'initRange: {}'.format(str(self.initRange)+'\n' if self.initRange else 'None\n')
		out += 'indexRange: {}'.format(str(self.indexRange)+'\n' if self.indexRange else 'None\n')
		out += 'contentLength: {}'.format(self.contentLength+'\n' if self.contentLength else 'None\n')
		out += 'averageBitrate: {}'.format(self.averageBitrate+'\n' if self.averageBitrate else 'None\n')
		out += 'approxDurationMs: {}'.format(self.approxDurationMs+'\n' if self.approxDurationMs else 'None\n')
		out += 'cipher: {}'.format(self.cipher+'\n' if self.cipher else 'None\n')
		return out
