import os
import random
import signal
import subprocess
from datetime import date
from time import sleep
from gpiozero import Button

videoPath = "https://drive.google.com/file/d/1mhGiDygE3X47jujLoYqewwhEJncvD5cP/view?usp=sharing"  # "/videos/Touch_the_temple.mp4"
rtmpPath = "rtmp://127.0.0.1:1936/live/xyz"

seasons = ["Winter", "Winter", "Spring", "Spring", "Spring", "Summer",
			"Summer", "Summer", "Fall", "Fall", "Fall", "Winter"]

switch = [Button(23), Button(24)]
mode = 1


def rmtp_stream():
	omxprocess = subprocess.Popen(['omxplayer', '-o', 'hdmi', rtmpPath],
								  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
	while switch[0].is_pressed and omxprocess.poll() is None:
		sleep(1)
	if omxprocess.poll() is None:
		omxprocess.stdin.write(b'q')


def still_music():
	music_list = os.listdir("/music")
	while True:
		random.shuffle(music_list)
		for song in music_list:
			song_path = os.path.join(musicPath, song)
			omxprocess = subprocess.Popen(['omxplayer', '-o', 'hdmi', song_path],
										  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
			while switch[1].is_pressed and omxprocess.poll() is None:
				sleep(1)
			if omxprocess.poll() is None:
				omxprocess.stdin.write(b'q')
			if not switch[1].is_pressed:
				break
		if not switch[1].is_pressed:
			break


def play_video():
	omxprocess = subprocess.Popen(['omxplayer', '--adev', 'hdmi', 'video/standby_video.mp4', '--loop', '-b'],
								  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
	while not switch[0].is_pressed and not switch[1].is_pressed and omxprocess.poll() is None:
		sleep(1)
	if omxprocess.poll() is None:
		omxprocess.stdin.write(b'q')
	sleep(5)


def download_video():
	dir = os.listdir("/video")
	# Download the file if it does not exist
	if len(dir) == 0:
		urllib.urlretrieve(videoPath, "standby_video.mp4")
	# if not os.path.isfile(filename):
		# urllib.urlretrieve(url, filename)


def load_framebuffer():
	today = date.today().strftime("%m/%d/%y")
	cur_season = seasons[int(today[0:2])]
	os.system('fbi -a --noverbose -T 1 -t 15 "/images/{}stakecenter.jpg"'.format(cur_season))


def run():
	print("Waiting for frame buffer to load")
	sleep(10)  # wait for the video drivers to start up so the frame buffer can be loaded
	print("Downloading video if missing")
	download_video()
	print("Download complete")
	load_framebuffer()
	while True:
		if switch[0].is_pressed:  # RTMP server
			rtmp_stream()
		elif switch[1].is_pressed:  # Music Only
			still_music()
		else:  # Touch the Temple
			play_video()


# Main program logic follows:
if __name__ == '__main__':
	run()
