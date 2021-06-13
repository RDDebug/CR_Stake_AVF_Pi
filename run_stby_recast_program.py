#  author: Jason Austin, Cedar Rapids Iowa Stake
#  date last modified: 12-jun-2021
import os
import random
import urllib
import signal
import subprocess
#import config
import google_drive_download as gdd
from datetime import date
from time import sleep
from gpiozero import Button
from configparser import ConfigParser

switch = [Button(23), Button(24)]
config = {}

def rmtp_stream():
	omxprocess = subprocess.Popen(['omxplayer', '-o', 'hdmi', config["rtmpPath"]],
								  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
	while switch[0].is_pressed and omxprocess.poll() is None:
		sleep(1)
	if omxprocess.poll() is None:
		omxprocess.stdin.write(b'q')


def still_music(control):
	music_list = os.listdir("music")
	while True:
		random.shuffle(music_list)
		for song in music_list:
			song_path = os.path.join("music", song)
			omxprocess = subprocess.Popen(['omxplayer', '-o', 'hdmi', song_path],
										  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
			if config["switch_used"] is True:
				while control.is_pressed and omxprocess.poll() is None:
					sleep(1)
			else:
				while omxprocess.poll() is None:
					sleep(1)
			if omxprocess.poll() is None:
				omxprocess.stdin.write(b'q')
			if not switch[1].is_pressed:
				break
		if not control.is_pressed:
			break


def play_video():
	omxprocess = subprocess.Popen(['omxplayer', '--adev', 'hdmi', 'video/{}'.format(config["video"]["title"]), '--loop', '-b'],
								  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
	while not switch[0].is_pressed and not switch[1].is_pressed and omxprocess.poll() is None:
		sleep(1)
	if omxprocess.poll() is None:
		omxprocess.stdin.write(b'q')
	sleep(5)


def download_video():
	if not os.path.exists('video/{}'.format(config["video"]["title"])):
		print("Downloading video {}".format(config["video"]["title"]))
		gdd.download_file_from_google_drive(config["video"]["drive_id"], 'video/{}'.format(config["video"]["title"]))
		print("Download complete")


def load_framebuffer():
	if config["use_temple_image"] is True:
		image = "temple.jpg"
	else:
		today = date.today().strftime("%m/%d/%y")
		cur_season = config["seasons"][int(today[0:2])]
		image = "{}stakecenter.jpg".format(cur_season)

	os.system('fbi -a --noverbose -T 1 -t 15 "images/{}"'.format(image))


def load_config():
	global config
	config_object = ConfigParser()
	if not os.path.exists("config.ini"):
		config_object["CONFIG"] = {
			"switch_used": True,
			"video_enabled": False,
			"rmtp_enabled": True,
			"use_temple_image": False,
			"music_enabled": True,

			"video": {"title": "touch_the_temple.mp4","drive_id": "1mhGiDygE3X47jujLoYqewwhEJncvD5cP"},
			"rtmpPath": "rtmp://127.0.0.1:1936/live/xyz",

			"seasons": ["winter", "winter", "spring", "spring", "spring", "summer",
				   "summer", "summer", "fall", "fall", "fall", "winter"]
		}
		with open('config.ini', 'w') as conf:
			config_object.write(conf)
	else:
		config_object.read("config.ini")

	config = config_object["CONFIG"]


def run_switch():
	download_video()
	load_framebuffer()
	while True:
		if switch[0].is_pressed:  # RTMP server
			if config["rmtp_enabled"] is True:
				rmtp_stream()
			else:
				still_music(switch[0])
		elif switch[1].is_pressed:  # Music Only
			if config["music_enabled"] is True:
				still_music(switch[1])
			else:
				sleep(10)
		else:  # Touch the Temple
			play_video()


def run_no_switch():
	if config["video_enabled"] is True:
		print("Downloading video if missing")
		download_video()
	load_framebuffer()
	while True:
		if config["video_enabled"] is True:
			play_video()
		else:
			if config["music_enabled"] is True:
				still_music(switch[0])
			else:
				sleep(10)


# Main program logic follows:
if __name__ == '__main__':
	print("Waiting for frame buffer to load")
	for cnt in range(10, 0, -1):
		print(cnt)
		sleep(1)  # wait for the video drivers to start up so the frame buffer can be loaded
	if config["switch_used"] is True:
		run_switch()
	else:
		run_no_switch()
