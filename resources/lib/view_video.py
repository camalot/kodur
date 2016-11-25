import sys
import urllib
import re
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
import http_request
import control
import utils
from player import player


class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.video_url = urllib.unquote_plus(params["video_url"])
        self.play_video()

    def play_video(self):
        # Get current list item details...
        title = unicode(xbmc.getInfoLabel("ListItem.Title"), "utf-8")
        thumbnail = xbmc.getInfoImage("ListItem.Thumb")
        plot = unicode(xbmc.getInfoLabel("ListItem.Plot"), "utf-8")
        genre = unicode(xbmc.getInfoLabel("ListItem.Genre"), "utf-8")
        total_time = unicode(xbmc.getInfoLabel("ListItem.EndTime"), "utf-8")
        # Show wait dialog while parsing data...
        dialog_wait = xbmcgui.DialogProgress()
        dialog_wait.create(control.lang(30504), title)

        if self.video_url is None:
            # Close wait dialog...
            dialog_wait.close()
            del dialog_wait

            # Message...
            xbmcgui.Dialog().ok(control.lang(30000), control.lang(30505))
            return

        # Close wait dialog...
        dialog_wait.close()
        del dialog_wait

        player().run({"url": self.video_url, "thumb": thumbnail, "plot": plot, "genre": genre, "title": title,
                    "endTime": total_time, "repeat": "Repeat One"})
        return
