from Player import Player
# from getkey import getkey, keys
import msvcrt
import sys
from itertools import cycle
from time import sleep
import threading
import argparse
from colorama import Fore
import os

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'
QUIT_SEARCH = False
LINE_BUFFER = 0

# Launches chrome with YouTube landing page
yt_music = Player()


def delete_lines(n=1):
	for _ in range(n):
		sys.stdout.write(CURSOR_UP_ONE)
		sys.stdout.write(ERASE_LINE)


def search_animation():
	for _ in cycle(['|', '/', '-', '\\']):
		if QUIT_SEARCH:
			sys.stdout.write('\r\033[K')
			sys.stdout.flush()
			return
		print(Fore.LIGHTCYAN_EX +  '\rSearching ' + _, end='\r'+ Fore.RESET)
		sleep(1)


def display_info():
	new_title = 'Idle'

	while True:

		try:
			title = yt_music.get_song_title()
		except:
			title = 'Idle'

		if new_title == title:
			continue
		else:
			global LINE_BUFFER
			delete_lines(LINE_BUFFER)
			LINE_BUFFER = 13

			try:
				sleep(5)
				has_playlist = yt_music.get_playlist()
				if not has_playlist:
					playlist = 'No playlist associated with this song.'
					LINE_BUFFER -= 4
				else:
					playlist = '\n'.join([track for track in has_playlist.values()])
			except:
				playlist = 'Idle'
				LINE_BUFFER -= 4

			controls = "New song: n\tPause: o\tNext song: p\tPrev song: i\tQuit: q\nSeek 5 seconds: a/d\t" \
					   "Volume: w/s\tMute: m\n " 

			print((Fore.LIGHTCYAN_EX + f'Now Playing: {Fore.WHITE + title + Fore.RESET}\n\n'+ Fore.RESET) + (Fore.LIGHTCYAN_EX + f'Playlist:\n{Fore.WHITE + playlist + Fore.RESET}\n\n'+ Fore.RESET) + (Fore.LIGHTCYAN_EX + f'Controls:\n{Fore.WHITE + controls + Fore.RESET}\r' + Fore.RESET))

			new_title = title
			sleep(1)


def parse_args():
	"""
	Parse winiplayer args
	:return:
	"""
	parser = argparse.ArgumentParser(description='winiplayer - music from terminal')
	parser.add_argument('-s', '--song', type=str, help='Song name', required=True)
	parser.add_argument('-c', '--config', action='store_true')

	return parser.parse_args()


def application(args):
	"""
	Event loop for Player
	:param args: Arguments from command line: song name (required), config (optional)
	:return:
	"""
	if args.config:
		res = yt_music.auth()
		if res == 0:
			print('Using stored credentials.')
		else:
			print('Logged in.')

	inf = threading.Thread(target=display_info)
	inf.start()
	global QUIT_SEARCH
	QUIT_SEARCH = False
	anim = threading.Thread(target=search_animation)
	anim.start()
	QUIT_SEARCH = yt_music.search(song=args.song)
	anim.join()

	key = ''

	while True:
		if msvcrt.kbhit():
			key = msvcrt.getch()
			key = key.decode('utf-8')

			if key == 'n':
				song = input(Fore.WHITE + 'Search new song: ' + Fore.RESET)
				delete_lines(1)			
				QUIT_SEARCH = False
				anim = threading.Thread(target=search_animation)
				anim.start()
				QUIT_SEARCH = yt_music.search(song=song)
				anim.join()

			elif key == 'i':
				yt_music.prev()

			elif key == 'o':
				yt_music.play_pause()

			elif key == 'p':
				yt_music.next()

			elif key == 'm':
				yt_music.mute()

			elif key == 'a':
				yt_music.backward()

			elif key == 'd':
				yt_music.forward()

			elif key == 'w':
				yt_music.volume_up()

			elif key == 's':
				yt_music.volume_down()

			elif key == 'q':
				delete_lines(LINE_BUFFER)
				yt_music.quit()
				pid = os.getpid()
				os.system(f"taskkill /pid {pid} /f")
				#return


if __name__ == "__main__":

	arguments = parse_args()
	# print(arguments)
	application(arguments)
