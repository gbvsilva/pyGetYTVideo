# python3
import requests
import re
from subprocess import Popen, PIPE
from media import *
	
if __name__ == '__main__':
	while True:
		link = input('Digite uma URL do YouTube: ')
		user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
		headers = {'User-Agent': user_agent}
		video_id = None
		if link.startswith('https://www.youtube.com/watch?v=') or link.startswith('https://youtube.com/watch?v=') \
			or link.startswith('https://youtu.be/'):
			
			response = requests.get(link, data=None, headers=headers)
			
			html = response.text
			try:
				video_src = html.split('itag":18,"url":"')[1].split('"')[0].replace('\\u0026', '&')
			except:
				print('Video com direitos autorais!')
				#TODO: talvez seja preciso fazer captura em separado do audio e do video
				continue
	
			print('Video Source: %s' % video_src)
			open_video = input('\nAbrir video? (y/N) ')
			if open_video.lower() == 'n':
				break
			else:
				p1 = Popen(['which', 'x-www-browser'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
				browser = p1.stdout.read()
				browser = browser[:-1] # removing new line
				p2 = Popen([browser, video_src], stdout=PIPE, stderr=PIPE, stdin=PIPE)
		else:
			print('Link inválido!')
