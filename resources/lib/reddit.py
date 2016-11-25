import sys
import control
import utils
import urllib
import xbmc


class Main:

    def __init__(self):
        self.params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        if self.params["action"] == "reddit_add":
            utils.add_subreddit(None)

        self.render_reddit_list()
        return

    def render_reddit_list(self):
        utils.set_no_sort()
        utils.add_directory(utils.text_green % control.lang(30502), utils.icon_settings, None,
                            "%s?action=settings" % (sys.argv[0]))

        utils.add_directory(utils.text_heading % (control.lang(30508)), utils.icon_folder, None,
                            "%s?action=reddit_add" % (sys.argv[0]))

        reddits = utils.get_subreddits()
        for sr in reddits:
            utils.add_directory(sr.title(), utils.icon_folder, None,
                                "%s?action=gallery&section=%s&type=reddit" % (
                                    sys.argv[0], urllib.quote_plus(sr.title())))
        control.directory_end(force_thumb=False)
        return
