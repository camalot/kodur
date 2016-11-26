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
        self.gallery_type = urllib.unquote_plus(params.get("type", 'default'))
        self.section = urllib.unquote_plus(params.get("section", ''))
        self.sort = urllib.unquote_plus(params.get("sort", ''))
        if self.section == '':
            self.display_section_choice()
        elif self.sort == '':
            self.display_sort_choice()
        else:
            self.browse_gallery(self.gallery_type)
        return

    def display_section_choice(self, close_directory=True):
        epoch_time = int(time.time())

        utils.add_directory(utils.text_blue % control.lang(30601), utils.icon_folder, None,
                            "%s%s?action=gallery&section=hot" % (sys.argv[0], epoch_time))
        utils.add_directory(utils.text_blue % control.lang(30602), utils.icon_folder, None,
                            "%s%s?action=gallery&section=top" % (sys.argv[0], epoch_time))
        utils.add_directory(utils.text_blue % control.lang(30603), utils.icon_folder, None,
                            "%s%s?action=gallery&section=user" % (sys.argv[0], epoch_time))
        if close_directory:
            control.directory_end(force_thumb=False)
        return

    def display_sort_choice(self, close_directory=True):
        if not self.gallery_type == 'reddit':
            utils.add_directory(utils.text_blue % control.lang(30604), utils.icon_folder, None,
                                "%s?action=gallery&section=%s&sort=viral" % (sys.argv[0], self.section))
        utils.add_directory(utils.text_blue % control.lang(30605), utils.icon_folder, None,
                            "%s?action=gallery&section=%s&sort=top&type=%s" % (sys.argv[0], self.section, self.gallery_type))
        utils.add_directory(utils.text_blue % control.lang(30606), utils.icon_folder, None,
                            "%s?action=gallery&section=%s&sort=time&type=%s" % (sys.argv[0], self.section, self.gallery_type))
        if self.section == 'user':
            utils.add_directory(utils.text_blue % control.lang(30607), utils.icon_folder, None,
                                "%s?action=gallery&section=%s&sort=rising" % (sys.argv[0], self.section))

        if close_directory:
            control.directory_end(force_thumb=False)
        return

    def browse_gallery(self, gallery_type=None):
        epoch_time = int(time.time())

        api = imgur.Api()
        if gallery_type == 'reddit':
            data = api.get_reddit_gallery(self.section, self.sort, "all", self.page)
        else:
            data = api.get_gallery(self.section, self.sort, "all", self.page, False)
        for g in data["galleries"]:
            utils.add_gallery_item(g)

        next_page = self.page + 1
        utils.add_next_page("%s%s?action=gallery&page=%s&section=%s&sort=%s&type=%s" %
                            (sys.argv[0], epoch_time, next_page, self.section, self.sort, self.gallery_type),
                            next_page + 1)

        control.directory_end(force_thumb=True)
