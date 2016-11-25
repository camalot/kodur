import utils
import http_request
import json
import os
import xbmc

class Api:
    url_root = "https://api.imgur.com/3"

    url_gallery = "%s/gallery/%s/%s/%s/%s?showViral=%s"
    url_reddit_gallery = "%s/gallery/r/%s/%s/%s/%s"
    url_meme_gallery = "%s/g/memes/%s/%s/%s"
    url_random_gallery = "%s/gallery/random/random/%s"

    url_album = "%s/album/%s"
    url_image = "%s/image/%s"
    url_meme_image = "%s/memes/%s"
    url_image_medium = "http://i.imgur.com/%sm.png"
    url_image_thumb = "http://i.imgur.com/%sm.png"
    __client_id__ = "#{CLIENT_ID}"
    __client_id_env__ = os.environ.get("KODUR_CLIENT_ID")

    video_types = ["image/gif"]

    def __init__(self):

        # this is for local development so the client id does not exist in code
        # #{CLIENT_ID} will get replaced by CI
        if self.__client_id__ == '#{CLIENT_ID}' and self.__client_id_env__ is not None:
            self.__client_id__ = self.__client_id_env__
        return

    def get_gallery(self, section='hot', sort='viral', window='all', page=0, show_viral=True):
        url = self.url_gallery % (self.url_root, section, sort, window, page, show_viral)
        result = http_request.get(url, self._authorization_header())
        json_obj = json.loads(result)["data"]

        return {"galleries": json_obj, "totalResultCount": len(json_obj)}

    def get_reddit_gallery(self, reddit, sort='time', window='all', page=0):
        url = self.url_reddit_gallery % (self.url_root, reddit, sort, window, page)
        result = http_request.get(url, self._authorization_header())
        json_obj = json.loads(result)["data"]

        return {"galleries": json_obj, "totalResultCount": len(json_obj)}

    def get_random_gallery(self, page=0):
        url = self.url_random_gallery % (self.url_root, page)
        result = http_request.get(url, self._authorization_header())
        json_obj = json.loads(result)["data"]

        return {"galleries": json_obj, "totalResultCount": len(json_obj)}

    def get_album(self, album_id):
        url = self.url_album % (self.url_root, album_id)
        result = http_request.get(url, self._authorization_header())
        json_obj = json.loads(result)["data"]

        return {"album": json_obj}

    def get_image(self, image_id):
        url = self.url_image % (self.url_root, image_id)
        result = http_request.get(url, self._authorization_header())
        json_obj = json.loads(result)["data"]

        return {"image": json_obj}

    def get_meme_gallery(self, sort='viral', window='all', page=0):
        url = self.url_meme_gallery % (self.url_root, sort, window, page)
        result = http_request.get(url, self._authorization_header())
        json_obj = json.loads(result)["data"]

        return {"memes": json_obj, "totalResultCount": len(json_obj)}

    def get_meme_image(self, image_id):
        url = self.url_image % (self.url_root, image_id)
        result = http_request.get(url, self._authorization_header())
        json_obj = json.loads(result)["data"]

        return {"meme": json_obj}

    def _authorization_header(self):
        return [{"key": "Authorization", "value": "Client-ID %s" % self.__client_id__}]
