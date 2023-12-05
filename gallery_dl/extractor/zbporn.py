# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://zbporn.com/"""

from .common import GalleryExtractor
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?zbporn\.com"


class ZbpornGalleryExtractor(GalleryExtractor):
    category = 'zbporn'
    directory_fmt = ('{category}', '{title}')
    pattern = (r"(?:https?://)?(?:www\.)?zbporn\.com"
               r"/albums/(\d+)/([a-zA-Z0-9\-_#%]+)")
    root = 'https://zbporn.com'
    example = 'https://zbporn.com/albums/123456/title-of-album/'

    def __init__(self, match):
        self.gallery_id = match.group(1)
        self.title = match.group(2)
        url = "{}/albums/{}/{}/".format(
            self.root, self.gallery_id, self.title)
        GalleryExtractor.__init__(self, match, url)

    def images(self, page):
        extr = text.extr(page,
                         '"gallery-holder js-album">', "</div>")
        return [(i, None)
                for i in text.extract_iter(extr, 'href="', '"')]

    def metadata(self, page):
        extr = text.extract_from(page, page.index('class="view-info">'))
        return {
            "title": self.title,
            "gallery_id": self.gallery_id,
            "user": text.remove_html(extr('icon-profile">', "</span>")),
            "tags": text.split_html(extr('icon-categories">', "</div>")),
        }
