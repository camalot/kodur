import sys
import control
import utils
import urllib
import json
import xbmc
import xbmcgui
from player import player


class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.image_url = urllib.unquote_plus(params["image_url"])
        self.view_image()
        return

    def view_image(self):
        title = unicode(xbmc.getInfoLabel("ListItem.Title"), "utf-8")
        thumbnail = xbmc.getInfoImage("ListItem.Thumb")
        player().view({"url": self.image_url, "thumb": thumbnail, "title": title})
        return
