switch_used = True  # if true, the script will assume a 2 way switch will connect GPIO 23 and 24 to ground
video_enabled = False  # only used if switch_used is False
rtmp_enabled = True  # if False, switch in position 1 will default to still/music
use_temple_image = False  # if True, the still image used will be the Nauvoo temple
music_enabled = True  # if True, music will be played along with the still image

video = {"title": "touch_the_temple.mp4",
		 "drive_id": "1mhGiDygE3X47jujLoYqewwhEJncvD5cP"}
rtmpPath = "rtmp://127.0.0.1:1936/live/xyz"

seasons = ["winter", "winter", "spring", "spring", "spring", "summer",
			"summer", "summer", "fall", "fall", "fall", "winter"]

# default:
# # switch_used = True
# # video_enabled = False
# # rtmp_enabled = True
# # use_temple_image = False
# # music_enabled = True

# video = {"title": "touch_the_temple.mp4",
# 		 "drive_id": "1mhGiDygE3X47jujLoYqewwhEJncvD5cP"}
# rtmpPath = "rtmp://127.0.0.1:1936/live/xyz"

# seasons = ["Winter", "Winter", "Spring", "Spring", "Spring", "Summer",
# 			"Summer", "Summer", "Fall", "Fall", "Fall", "Winter"]