from configparser import ConfigParser


def yes_or_no(request):
    rtn = None
    while rtn is None:
        user_input = input('{} (y/n):'.format(request))
        rtn = True if user_input.lower == 'y' else None
        rtn = False if user_input.lower == 'n' else rtn
    return rtn


def configure_rtmp_path():
    port = input("What port will the RTMP server use (default: 1936)")
    site = input("what site will your RTMP sender be targeting (default: xyz)")

    if port == "":
        port = "1936"
    if site == "":
        site = "xyz"

    return "rtmp://127.0.0.1:{}/live/{}".format(port, site)


def configure_video():
    title = input("What is the title of the video (default: standby.mp4)")
    id = input("What is the Google drive ID for the target video (default: 1a42sJBMgshSQ94A_fA7jYJFZu0SlODVg")

    if title == "":
        title = "standby.mp4"
    if id == "":
        id = "1a42sJBMgshSQ94A_fA7jYJFZu0SlODVg"

    return {"title": title, "drive_id": id}


def month_to_season(month, season):
    new_season = input("What season is it in the month of {} (default: {}".format(month, season))
    if new_season == "":
        new_season = season


def configure_seasons:
    seasons = [("January", "winter"),
               ("February", "winter"),
               ("March", "spring"),
               ("April", "spring"),
               ("May", "spring"),
               ("June", "summer"),
               ("July", "summer"),
               ("August", "summer"),
               ("September", "fall"),
               ("October", "fall"),
               ("November", "fall"),
               ("December", "winter")]
    new_seasons = []
    for (month, season) in seasons:
        temp_season = input("What season is it in the month of {} (default: {}".format(month, season))
        new_seasons.append(temp_season if not temp_season == "" else season)
    return new_seasons

def build_config():
    switch_used = yes_or_no("Your setup uses a switch to enable multiple functions")
    if switch_used is False:
        video_enabled = yes_or_no("Your setup will play a video, rather than music and a still image")
        rtmp_enabled = False
    else:
        video_enabled = False
        rtmp_enabled = yes_or_no("You setup will be configured to accept and display external RTMP stream")
    if video_enabled is False:
        use_temple_image = yes_or_no("Your setup will display a still of a temple, rather than a seasonal image of the stake building")
        music_enabled = yes_or_no("While displaying a still image, your setup will play music")
        video = False
        rtmpPath = yes_or_no("You set up will use the default RTMP network path")
        if use_temple_image is False:
            seasons = yes_or_no("Your seasons align with those in Iowa")
        else:
            seasons = True
    else:
        use_temple_image = False
        music_enabled = False
        video = yes_or_no("Your set up will use the default video, 'touch the temple', provided by the stake")
        rtmpPath = False
        seasons = True

    video_config = {"title": "touch_the_temple.mp4", "drive_id": "1a42sJBMgshSQ94A_fA7jYJFZu0SlODVg"} if video is True else configure_video()
    rtmp_config = "rtmp://127.0.0.1:1936/live/xyz" if rtmpPath is True else configure_rtmp_path()
    season_config = ["winter", "winter", "spring", "spring", "spring", "summer", "summer", "summer", "fall", "fall", "fall", "winter"] if seasons is True else configure_seasons()

    config_object["CONFIG"] = {
        "switch_used": switch_used,
        "video_enabled": video_enabled,
        "rmtp_enabled": rtmp_enabled,
        "use_temple_image": use_temple_image,
        "music_enabled": music_enabled,

        "video": video_config,
        "rtmpPath": rtmp_config,

        "seasons": season_config
    }


def build_default_config():
    object = ConfigParser()
    object["CONFIG"] = {
        "switch_used": True,
        "video_enabled": False,
        "rmtp_enabled": True,
        "use_temple_image": False,
        "music_enabled": True,

        "video": {"title": "touch_the_temple.mp4", "drive_id": "1a42sJBMgshSQ94A_fA7jYJFZu0SlODVg"},
        "rtmpPath": "rtmp://127.0.0.1:1936/live/xyz",

        "seasons": ["winter", "winter", "spring", "spring", "spring", "summer",
                    "summer", "summer", "fall", "fall", "fall", "winter"]
    }
    with open('config.ini', 'w') as conf:
        object.write(conf)

if __name__ == '__main__':
    new_config = True
    if os.path.exists("config.ini"):
        config_object = ConfigParser()
        config_object.read("config.ini")
        print("Current config file:\n{}".format(config_object["CONFIG"]))
        new_config = yes_or_no("Overwrite current configs")
    if yes_or_no("Use default config file") is True
        build_default_config()
    elif new_config:
        build_config()


