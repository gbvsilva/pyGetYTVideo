# python3
import urllib.request
import re
from subprocess import Popen, PIPE
from media import *
	

if __name__ == '__main__':

	link = input()
	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
	headers = {'User-Agent': user_agent}
	video_id = None
	if link.startswith('https://www.youtube.com/watch?v=') or link.startswith('https://youtube.com/watch?v='):
		video_id = re.search('v=(.+)', link).group(1)
	elif link.startswith('https://youtu.be/'):
		video_id = re.search('be/(.+)', link).group(1)
	if video_id:
		#print('Video ID -> '+video_id)
		while True:
			req = urllib.request.Request('https://www.youtube.com/get_video_info?&video_id='+video_id, data=None, headers=headers)
			with urllib.request.urlopen(req) as response:
				html = response.read()
				parsed_html = urllib.parse.unquote(html.decode())
				data = parsed_html.split('&')
				r = re.compile('url=')
				url = list(filter(r.match, data))
				#print(url)
				url = urllib.parse.unquote(url[0])
				r = re.compile('s=')
				s = list(filter(r.match, data))
				#print(s)
				s = urllib.parse.unquote(s[0])
				#print(url)
				url = url[4:]
				s = s[2:]
				#print(s)
				#video = Media(link, html[i:i+j].decode().translate({ord('\\'): None}))
				#exit()
				#print("==== Video Info ====")
				#print(video)
				
				if len(s) == 106 and '=' in s and s.index('=') <= 100:
					if '2IxgL' in s:
						sig = list(s)
						sig.reverse()
						sig[sig.index('=')] = sig[-1]
						sig[-1] = '='
						video_url = url+'&sig='+''.join(sig[2:])
						print('Video URL: {}'.format(video_url if video_url else 'None'))
						open_video = input('\nOpen video? (Y/N) ')
						if open_video.lower() == 'y':
							p1 = Popen(['which', 'x-www-browser'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
							browser = p1.stdout.read()
							browser = browser[:-1] # removing new line
							p2 = Popen([browser, video_url], stdout=PIPE, stderr=PIPE, stdin=PIPE)
						break
	else:
		print('Invalid link!')
