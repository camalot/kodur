import sys
import control
import utils
import urllib
import xbmc
import imgur
import json
import xbmc

class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        album_id = params["id"]
        utils.set_no_sort()
        api = imgur.Api()

        data = api.get_album(album_id)["album"]
        images = data["images"]
        for img in images:
            if img["type"] not in api.video_types:
                xbmc.log("not video")
                image = img["link"]
                thumb = api.url_image_thumb % img["id"]
                utils.add_image(utils.text_blue % img["title"], thumb, image)
            else:
                url = img["mp4"]
                thumb = api.url_image_thumb % img["id"]
                utils.add_video(utils.text_blue % img["title"], thumb, url)

        control.directory_end(force_thumb=True)
        return
