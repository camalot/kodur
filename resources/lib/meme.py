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
        self.params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        utils.set_no_sort()

        if "sort" not in self.params or self.params["sort"] is None:
            self.display_sort_choice()
        else:
            self.browse_gallery()
        return

    def display_sort_choice(self, close_directory=True):
        utils.add_directory(utils.text_blue % control.lang(30604), utils.icon_folder, None,
                            "%s?action=meme&sort=viral" % (sys.argv[0]))
        utils.add_directory(utils.text_blue % control.lang(30605), utils.icon_folder, None,
                            "%s?action=meme&sort=top" % (sys.argv[0]))
        utils.add_directory(utils.text_blue % control.lang(30606), utils.icon_folder, None,
                            "%s?action=meme&sort=time" % (sys.argv[0]))

        if close_directory:
            control.directory_end(force_thumb=False)
        return

    def browse_gallery(self):
        api = imgur.Api()
        data = api.get_meme_gallery(self.params["sort"], "day", 0)
        for g in data["memes"]:
            if "cover" in g:
                thumb = api.url_image_medium % g["cover"]
                icon = api.url_image_thumb % g["cover"]
                utils.add_directory(g["title"], icon, thumb, "%s?action=album&id=%s" % (sys.argv[0], g["id"]))
            else:
                if g["type"] not in api.video_types:
                    image = g["link"]
                    thumb = api.url_image_thumb % g["id"]
                    utils.add_image(utils.text_blue % g["title"], thumb, image)
                else:
                    url = g["mp4"]
                    thumb = api.url_image_thumb % g["id"]
                    utils.add_video(utils.text_blue % g["title"], thumb, url)

        control.directory_end(force_thumb=True)
