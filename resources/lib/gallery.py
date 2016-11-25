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

        self.type = urllib.unquote_plus(self.params.get("type", 'default'))
        self.section = urllib.unquote_plus(self.params.get("section", ''))
        self.sort = urllib.unquote_plus(self.params.get("sort", ''))
        if self.section == '':
            self.display_section_choice()
        elif self.sort == '':
            self.display_sort_choice()
        else:
            self.browse_gallery(self.type)
        return

    def display_section_choice(self, close_directory=True):
        utils.add_directory(utils.text_blue % control.lang(30601), utils.icon_folder, None,
                            "%s?action=gallery&section=hot" % (sys.argv[0]))
        utils.add_directory(utils.text_blue % control.lang(30602), utils.icon_folder, None,
                            "%s?action=gallery&section=top" % (sys.argv[0]))
        utils.add_directory(utils.text_blue % control.lang(30603), utils.icon_folder, None,
                            "%s?action=gallery&section=user" % (sys.argv[0]))
        if close_directory:
            control.directory_end(force_thumb=False)
        return

    def display_sort_choice(self, close_directory=True):
        if not self.type == 'reddit':
            utils.add_directory(utils.text_blue % control.lang(30604), utils.icon_folder, None,
                                "%s?action=gallery&section=%s&sort=viral" % (sys.argv[0], self.section))
        utils.add_directory(utils.text_blue % control.lang(30605), utils.icon_folder, None,
                            "%s?action=gallery&section=%s&sort=top&type=%s" % (sys.argv[0], self.section, self.type))
        utils.add_directory(utils.text_blue % control.lang(30606), utils.icon_folder, None,
                            "%s?action=gallery&section=%s&sort=time&type=%s" % (sys.argv[0], self.section, self.type))
        if self.section == 'user':
            utils.add_directory(utils.text_blue % control.lang(30607), utils.icon_folder, None,
                                "%s?action=gallery&section=%s&sort=rising" % (sys.argv[0], self.section))

        if close_directory:
            control.directory_end(force_thumb=False)
        return

    def browse_gallery(self, type=None):
        api = imgur.Api()
        if type == 'reddit':
            data = api.get_reddit_gallery(self.section, self.sort, "all", 0)
        else:
            data = api.get_gallery(self.section, self.sort, "all", 0, False)
        for g in data["galleries"]:
            xbmc.log(json.dumps(g))
            if "cover" in g:
                xbmc.log("album")
                thumb = api.url_image_medium % g["cover"]
                icon = api.url_image_thumb % g["cover"]
                utils.add_directory(g["title"], icon, thumb, "%s?action=album&id=%s" % (sys.argv[0], g["id"]))
            else:
                xbmc.log("NOT album")
                if g["type"] not in api.video_types:
                    image = g["link"]
                    thumb = api.url_image_thumb % g["id"]
                    utils.add_image(utils.text_blue % g["title"], thumb, image)
                else:
                    # not all have mp4
                    if "mp4" in g:
                        url = g["mp4"]
                    elif "gifv" in g:
                        url = g["gifv"]
                    else:
                        url = g["link"]
                    thumb = api.url_image_thumb % g["id"]
                    utils.add_video(utils.text_blue % g["title"], thumb, url)

        control.directory_end(force_thumb=True)
