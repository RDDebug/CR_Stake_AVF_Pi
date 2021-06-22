#  author: Jason Austin, Cedar Rapids Iowa Stake
#  date last modified: 12-jun-2021
import os
import random
import urllib
import signal
import subprocess
import google_drive_download as gdd
from datetime import date
from time import sleep
from gpiozero import Button
import build_config
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
            if config["switch_used"] == "True":
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
    video_config = eval(config["video"])
    omxprocess = subprocess.Popen(['omxplayer', '--adev', 'hdmi', 'video/{}'.format(video_config["title"]), '--loop', '-b'],
                                  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
    while not switch[0].is_pressed and not switch[1].is_pressed and omxprocess.poll() is None:
        sleep(1)
    if omxprocess.poll() is None:
        omxprocess.stdin.write(b'q')
    sleep(5)


def download_video():
    video_config = eval(config["video"])
    if not os.path.exists('video/{}'.format(video_config["title"])):
        print("Downloading video {}".format(video_config["title"]))
        try_again = True
        while try_again:
            try:
                gdd.download_file_from_google_drive(video_config["drive_id"], 'video/{}'.format(video_config["title"]))
                print("Download complete")
                try_again = False
            except:
                print("Bad connection, trying again")
                sleep(5)


def load_framebuffer():
    if config["use_temple_image"] == "True":
        image = "temple.jpg"
    else:
        seasons = eval(config["seasons"])
        today = date.today().strftime("%m/%d/%y")
        cur_season = seasons[int(today[0:2])]
        image = "{}stakecenter.jpg".format(cur_season)

    os.system('fbi -a --noverbose -T 1 -t 15 "images/{}"'.format(image))


def load_config():
	global config
	config_object = ConfigParser()
	if not os.path.exists("config.ini"):
		build_config.build_default_config()
	config_object.read("config.ini")
	config = config_object["CONFIG"]


def run_switch():
	download_video()
	load_framebuffer()
	while True:
		if switch[0].is_pressed:  # RTMP server
			if config["rmtp_enabled"] == "True":
				rmtp_stream()
			else:
				still_music(switch[0])
		elif switch[1].is_pressed:  # Music Only
			if config["music_enabled"] == "True":
				still_music(switch[1])
			else:
				sleep(10)
		else:  # Touch the Temple
			play_video()


def run_no_switch():
	if config["video_enabled"] == "True":
		print("Downloading video if missing")
		download_video()
	load_framebuffer()
	while True:
		if config["video_enabled"] == "True":
			play_video()
		else:
			if config["music_enabled"] == "True":
				still_music(switch[0])
			else:
				sleep(10)


# Main program logic follows:
if __name__ == '__main__':
	print("Waiting for frame buffer to load")
	for cnt in range(10, 0, -1):
		print(cnt)
		sleep(1)  # wait for the video drivers to start up so the frame buffer can be loaded
	load_config()
	if config["switch_used"] == "True":
		run_switch()
	else:
		run_no_switch()
