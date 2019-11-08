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
		if self.cipher and self.urlType == 'desktop':
			parsed_cipher = urllib.parse.unquote(self.cipher)
			if parsed_cipher.index('s=') < parsed_cipher.index('url='):
				url = re.search('url=(.+)', parsed_cipher).group(1)
				m = re.search('s=(.+?)LAu0026', parsed_cipher)
			else:
				url = re.search('url=(.+?)u0026', parsed_cipher).group(1)
				m = re.search('u0026s=(.+LA?)LA', parsed_cipher)
			
			sig = list(m.group(1))
			sig.reverse()
			char1 = ''
			char2 = ''
			# 104 for desktop YT website
			if len(sig) == 104 and '=' in sig:
				char1 = sig[-1]
				char2 = sig[53]
				sig[-1] = '='
				sig[53] = char1
				sig[43] = char2
				sig = ''.join(sig)
				self.url = url+'&sig='+sig
			else:
				print('Fail on get content!')
				self.url = None
		elif self.cipher and self.urlType == 'mobile':
			parsed_cipher = urllib.parse.unquote(self.cipher)
			if parsed_cipher.index('s=') < parsed_cipher.index('url='):
				url = re.search('url=(.+)', parsed_cipher).group(1)
				m = re.search('s=(.+?)u0026', parsed_cipher)
			else:
				url = re.search('url=(.+?)u0026', parsed_cipher).group(1)
				if parsed_cipher.index('26s=') < parsed_cipher.index('sp=sig'):
					m = re.search('u0026s=(.+?)u0026', parsed_cipher)
				else:
					m = re.search('u0026s=(.*)', parsed_cipher)

			sig = list(m.group(1))
			sig.reverse()
			print("sig -> "+''.join(sig))
			char1 = ''
			char2 = ''
			# 106 for mobile YT website
			if sig.index("=") > -1 and sig.index("=") < 50:
				sig[sig.index("=")] = sig[-1]
				sig[-1] = '='
				sig[41] = sig[0]
			else:
				sig[89] = sig[105]
				char1 = sig[52]
				#char2 = sig[52]
				sig[52] = sig[0]
				sig[40] = char1
				del sig[-3:-1]
				del sig[-1]
			del sig[0:3]
			sig[0] = 'A'
			sig = ''.join(sig)
			print("new sig -> "+sig)
			self.url = url+'&sig='+sig
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
