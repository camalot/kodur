

import sys
import urllib
import os
import json
import xbmc
import xbmcgui
import xbmcplugin
import control
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
import http_request
from datetime import timedelta

# https://api.imgur.com/endpoints

icon_folder = os.path.join(control.imagesPath, "folder.png")
icon_search = os.path.join(control.imagesPath, "search.png")
icon_next = os.path.join(control.imagesPath, "next-page.png")
icon_settings = os.path.join(control.imagesPath, "settings.png")

subreddits_file = xbmc.translatePath("special://profile/addon_data/%s/subreddits" % control.addonInfo("id"))


image_ext = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]

text_green = "[B][COLOR green][UPPERCASE]%s[/UPPERCASE][/COLOR][/B]"
text_blue = "[B][COLOR blue]%s[/COLOR][/B]"

text_topic = "[B][COLOR purple]%s[/COLOR][/B]"
text_heading = "[B][COLOR white][UPPERCASE]%s[/UPPERCASE][/COLOR][/B]"


def add_directory(text, icon, thumbnail, url):
    list_item = xbmcgui.ListItem(text, iconImage=icon, thumbnailImage=thumbnail)
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    control.addItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=True)
    return


def add_video(title, thumbnail, video_url):
    list_item = control.item(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    list_item.setInfo("video", {"Title": title, "Studio": "4Chan"})
    list_item.setProperty("ListItem.IsResumable", "true")
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    plugin_play_url = '%s?action=play&video_url=%s' % (sys.argv[0], urllib.quote_plus(video_url))
    control.addItem(handle=int(sys.argv[1]), url=plugin_play_url, listitem=list_item, isFolder=False)


def add_image(title, thumbnail, image_url):
    list_item = control.item(title, iconImage="DefaultPicture.png", thumbnailImage=thumbnail, path=image_url)
    list_item.setInfo(type="pictures", infoLabels={"title": title, "exif:path": image_url, "picturepath": image_url})
    list_item.setArt({"thumb": thumbnail})
    list_item.setProperty(u'fanart_image', image_url)
    plugin_play_url = '%s?action=view&image_url=%s' % (sys.argv[0], urllib.quote_plus(image_url))
    control.addItem(handle=int(sys.argv[1]), url=plugin_play_url, listitem=list_item)
    # control.addItem(handle=int(sys.argv[1]), url=image_url, listitem=list_item)


def add_slideshow_image(title, thumbnail, image_url):
    list_item = control.item(title, iconImage="DefaultPicture.png", thumbnailImage=thumbnail, path=image_url)
    list_item.setInfo(type="pictures", infoLabels={"title": title, "exif:path": image_url, "picturepath": image_url})
    list_item.setArt({"thumb": thumbnail})
    list_item.setProperty(u'fanart_image', image_url)
    # plugin_play_url = '%s?action=view&image_url=%s' % (sys.argv[0], urllib.quote_plus(image_url))
    # control.addItem(handle=int(sys.argv[1]), url=plugin_play_url, listitem=list_item)
    control.addItem(handle=int(sys.argv[1]), url=image_url, listitem=list_item)


def add_next_page(item_url, page):
    list_item = control.item(text_green % (control.lang(30500) % page),
                             iconImage=icon_next, thumbnailImage=icon_next)
    control.addItem(handle=int(sys.argv[1]), url=item_url, listitem=list_item, isFolder=True)
    return

def add_subreddit(subreddit):
    _init_subreddits_file()
    exists = False
    fh = open(subreddits_file, 'r')
    content = fh.readlines()
    fh.close()
    if subreddit:
        for line in content:
            if line.lower() == subreddit.lower():
                exists = True
        if not exists:
            fh = open(subreddits_file, 'a')
            fh.write(subreddit+'\n')
            fh.close()
    else:
        keyboard = xbmc.Keyboard('', control.lang(30508))
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            subreddit = keyboard.getText()
            for line in content:
                if line.lower() == subreddit.lower()+"\n":
                    exists = True
            if not exists:
                fh = open(subreddits_file, 'a')
                fh.write(subreddit+'\n')
                fh.close()


def remove_subreddit(subreddit):
    _init_subreddits_file()

    fh = open(subreddits_file, 'r')
    content = fh.readlines()
    fh.close()
    new_content = ""
    for line in content:
        if line != subreddit+'\n':
            new_content += line
    fh = open(subreddits_file, 'w')
    fh.write(new_content)
    fh.close()
    xbmc.executebuiltin("Container.Refresh")


def get_subreddits():
    _init_subreddits_file()
    content = ""
    entries = []
    if os.path.exists(subreddits_file):
        fh = open(subreddits_file, 'r')
        content = fh.read()
        fh.close()
        spl = content.split('\n')
        for i in range(0, len(spl), 1):
            if spl[i]:
                subreddit = spl[i].strip()
                entries.append(subreddit.title())
    entries.sort()
    # for entry in entries:
    #     if entry.lower() == "all":
    #         addDir(entry, entry.lower(), 'listSorting', "")
    #     else:
    #         addDirR(entry, entry.lower(), 'listSorting', "")
    return entries


def _init_subreddits_file():
    if not os.path.exists(subreddits_file):
        fh = open(subreddits_file, 'a')
        fh.close()
    return

def set_no_sort():
    control.sort(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
    return
