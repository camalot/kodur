import sys
import control
import utils
import urllib
import xbmc

class Main:
    def __init__(self):
        utils.set_no_sort()

        utils.add_directory(utils.text_green % control.lang(30502), utils.icon_settings, None,
                            "%s?action=settings" % (sys.argv[0]))

        utils.add_directory(utils.text_heading % (control.lang(30503)), utils.icon_folder, None,
                            "%s?action=gallery" % (sys.argv[0]))

        utils.add_directory(utils.text_heading % control.lang(30504), utils.icon_folder, None,
                            "%s?action=meme" % (sys.argv[0]))
        utils.add_directory(utils.text_heading % control.lang(30505), utils.icon_folder, None,
                            "%s?action=reddit" % (sys.argv[0]))
        utils.add_directory(utils.text_heading % control.lang(30506), utils.icon_folder, None,
                            "%s?action=random" % (sys.argv[0]))


        control.directory_end(force_thumb=False)
        return
