import os
import random
import urllib
import signal
import subprocess
import config
import google_drive_download as gdd
from datetime import date
from time import sleep
from gpiozero import Button

video_id = "1mhGiDygE3X47jujLoYqewwhEJncvD5cP"  # "/videos/Touch_the_temple.mp4"
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
			if config.switch_used is True:
				while switch[1].is_pressed and omxprocess.poll() is None:
					sleep(1)
			else:
				while omxprocess.poll() is None:
					sleep(1)
			if omxprocess.poll() is None:
				omxprocess.stdin.write(b'q')
			if not switch[1].is_pressed:
				break
		if not switch[1].is_pressed:
			break


def play_video():
	omxprocess = subprocess.Popen(['omxplayer', '--adev', 'hdmi', 'video/touch_the_temple.mp4', '--loop', '-b'],
								  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
	while not switch[0].is_pressed and not switch[1].is_pressed and omxprocess.poll() is None:
		sleep(1)
	if omxprocess.poll() is None:
		omxprocess.stdin.write(b'q')
	sleep(5)


def download_video():
	if not os.path.exists('video/touch_the_temple.mp4'):
		gdd.download_file_from_google_drive(video_id, "video/touch_the_temple.mp4")


def load_framebuffer():
	if use_temple_image is True:
		image = "temple"
	else:
		today = date.today().strftime("%m/%d/%y")
		cur_season = seasons[int(today[0:2])]
		image = "{}stakecenter.jpg".format(cur_season)

	os.system('fbi -a --noverbose -T 1 -t 15 "/images/{}"'.format(image))


def run_switch():
	print("Waiting for frame buffer to load")
	for cnt in range(10, 0, -1):
		print(cnt)
		sleep(1)  # wait for the video drivers to start up so the frame buffer can be loaded
	print("Downloading video if missing")
	download_video()
	print("Download complete")
	load_framebuffer()
	while True:
		if switch[0].is_pressed:  # RTMP server
			if config.rtmp_enabled is True:
				rtmp_stream()
			else:
				still_music()
		elif switch[1].is_pressed:  # Music Only
			if config.music_enabled is True:
				still_music()
			else:
				sleep(10)
		else:  # Touch the Temple
			play_video()


def run_no_switch():
	print("Waiting for frame buffer to load")
	for cnt in range(10, 0, -1):
		print(cnt)
		sleep(1)  # wait for the video drivers to start up so the frame buffer can be loaded
	load_framebuffer()
	while True:
		if config.video_enabled is True:
			play_video()
		else:
			if config.music_enabled is True:
				still_music()
			else:
				sleep(10)


# Main program logic follows:
if __name__ == '__main__':
	if config.switch_used is True:
		run_switch()
	else:
		run_no_switch()
