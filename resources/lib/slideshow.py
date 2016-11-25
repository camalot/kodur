import sys
import control
import utils
import urllib
import xbmc


class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.image_url = urllib.unquote_plus(params["image_url"])
        self.title = self.image_url.split("/")[-1]
        self.slideshow()
        return

    def slideshow(self):
        utils.add_image(self.title, self.image_url, self.image_url)
        control.directory_end()
        return
