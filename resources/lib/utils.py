

import sys
import urllib
import os
import json
import xbmc
import xbmcgui
import xbmcplugin
import control
import imgur
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
text_red = "[B][COLOR red]%s[/COLOR][/B]"

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


def add_image(title, thumbnail, image_url, slideshow=False):
    list_item = control.item(title, iconImage="DefaultPicture.png", thumbnailImage=thumbnail, path=image_url)
    list_item.setInfo(type="pictures", infoLabels={"title": title, "exif:path": image_url, "picturepath": image_url})
    list_item.setArt({"thumb": thumbnail})
    list_item.setProperty(u'fanart_image', image_url)
    if slideshow:
        control.addItem(handle=int(sys.argv[1]), url=image_url, listitem=list_item)
    else:
        plugin_play_url = '%s?action=view&image_url=%s' % (sys.argv[0], urllib.quote_plus(image_url))
        control.addItem(handle=int(sys.argv[1]), url=plugin_play_url, listitem=list_item)


def add_next_page(item_url, page):
    list_item = control.item(text_green % (control.lang(30500) % page),
                             iconImage=icon_next, thumbnailImage=icon_next)
    control.addItem(handle=int(sys.argv[1]), url=item_url, listitem=list_item, isFolder=True)
    return


def add_gallery_item(item):
    api = imgur.Api()
    allow_nsfw = control.setting("enable_nsfw") == 'true'

    if "cover" in item:
        thumb = api.url_image_medium % item["cover"]
        icon = api.url_image_thumb % item["cover"]
        add_directory(item["title"], icon, thumb, "%s?action=album&id=%s" % (sys.argv[0], item["id"]))
    else:
        is_nsfw = "nsfw" in item and item["nsfw"]
        if is_nsfw and not allow_nsfw:
            return

        text_dec = text_red if is_nsfw else text_blue

        if item["type"] not in api.video_types or not item["animated"]:
            image = item["link"]
            thumb = api.url_image_thumb % item["id"]

            add_image(text_dec % item["title"], thumb, image)
        else:
            # not all have mp4
            if "mp4" in item:
                url = item["mp4"]
            elif "gifv" in item:
                url = item["gifv"]
            else:
                url = item["link"]
            thumb = api.url_image_thumb % item["id"]
            add_video(text_dec % item["title"], thumb, url)
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
    return entries


def _init_subreddits_file():
    if not os.path.exists(subreddits_file):
        fh = open(subreddits_file, 'a')
        fh.close()
    return

def set_no_sort():
    control.sort(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
    return
