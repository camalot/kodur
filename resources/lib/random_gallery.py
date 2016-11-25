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

        self.page = int(urllib.unquote_plus(params.get("page", '0')))
        self.browse_gallery()
        return

    def browse_gallery(self):
        epoch_time = int(time.time())

        api = imgur.Api()
        data = api.get_random_gallery(self.page)
        for g in data["galleries"]:
            utils.add_gallery_item(g)

        next_page = self.page + 1
        utils.add_next_page("%s%s?action=random&page=%s" %
                            (sys.argv[0], epoch_time, next_page), next_page + 1)

        control.directory_end(force_thumb=True)
