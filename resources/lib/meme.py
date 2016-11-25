import sys
import control
import utils
import urllib
import time
import imgur
import json
import xbmc

class Main:
    def __init__(self):

        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        utils.set_no_sort()
        self.sort = urllib.unquote_plus(params.get("sort", ''))
        self.page = int(urllib.unquote_plus(params.get("page", '0')))

        if self.sort == '':
            self.display_sort_choice()
        else:
            self.browse_gallery()
        return

    def display_sort_choice(self, close_directory=True):
        epoch_time = int(time.time())

        utils.add_directory(utils.text_blue % control.lang(30604), utils.icon_folder, None,
                            "%s%s?action=meme&sort=viral" % (sys.argv[0], epoch_time))
        utils.add_directory(utils.text_blue % control.lang(30605), utils.icon_folder, None,
                            "%s%s?action=meme&sort=top" % (sys.argv[0], epoch_time))
        utils.add_directory(utils.text_blue % control.lang(30606), utils.icon_folder, None,
                            "%s%s?action=meme&sort=time" % (sys.argv[0], epoch_time))

        if close_directory:
            control.directory_end(force_thumb=False)
        return

    def browse_gallery(self):
        api = imgur.Api()
        data = api.get_meme_gallery(self.sort, "all", self.page)
        for g in data["memes"]:
            utils.add_gallery_item(g)

        control.directory_end(force_thumb=True)
