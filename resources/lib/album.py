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
            utils.add_gallery_item(img)

        control.directory_end(force_thumb=True)
        return
