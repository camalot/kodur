
##############################################################################
#
# 4Chan plugin for Kodi
# https://mva.microsoft.com
#
# Version 1.0
#
#
# https://github.com/camalot/plugin.image.kochandi
#
#


import os
import sys
import urlparse
import xbmc
import xbmcaddon

__addon__ = "Kodur"
__author__ = "Ryan Conrad"
__url__ = "https://github.com/camalot/plugin.image.kodur"
__date__ = "11/23/2016"
__version__ = "1.0"


addon_path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path'))
lib_path = xbmc.translatePath(os.path.join(addon_path, 'resources', 'lib'))
sys.path.append(lib_path)

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
action = params.get('action', 'home')

if action is None or action == '':
    print "no action found: triggering default"
    action = 'home'

xbmc.log("url: %s" % sys.argv[2])

if action == 'home':
    import home as plugin
elif action == 'album':
    import album as plugin
elif action == 'gallery':
    import gallery as plugin
elif action == 'meme':
    import meme as plugin
elif action == 'reddit' or action == 'reddit_add':
    import reddit as plugin
elif action == 'view':
    import view_image as plugin
elif action == 'play':
    import view_video as plugin
elif action == 'settings':
    import settings as plugin
elif action == 'slideshow':
    import slideshow as plugin
else:
    import home as plugin

plugin.Main()
