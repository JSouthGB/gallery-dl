# -*- coding: utf-8 -*-

# Copyright 2023 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://homepornbay.com/"""

from .common import GalleryExtractor, Message
from .. import text


class HomepornbayGalleryExtractor(GalleryExtractor):
    category = "homepornbay"
    root = "https://m.homepornbay.com"
    directory_fmt = ("{category}", "{title}")
    archive_fmt = "{date:%Y-%m-%d}_{category}_{filename}"
    pattern = (r"(?:https?://)?m.homepornbay\.com/"
               r"(album)/([A-Za-z0-9]+(-[A-Za-z0-9]+)+)")
    example = "https://m.homepornbay.com/album/AN-ALBUM"

    def __init__(self, match):
        self.gallery_title = match.group(2)
        url = "{}/album/{}".format(
            self.root, self.gallery_title)
        GalleryExtractor.__init__(self, match, url)

    def items(self):
        page = self.request(self.gallery_url).text
        imgs = self.images(page)
        data = self.metadata(page)

        yield Message.Directory, data

        for num, img in enumerate(imgs, start=1):
            path = text.nameext_from_url(img, {
                "num": num,
                "gallery_title": self.gallery_title,
                "title": data["title"],
                "date": data["date"],
                "count": data["count"]
            })
            yield Message.Url, img, path

    def images(self, page):
        imgs = text.extr(page, 'class="galleryView"', "</table>")
        return [text.ensure_http_scheme(i) for i in text.extract_iter(
            imgs, 'href="//', '"')]

    def metadata(self, page):
        extr = text.extract_from(page)
        return {
            "gallery_title": self.gallery_title,
            "title"        : extr("<title>", " - "),
            "date"         : text.parse_datetime(
                extr("<span>Added: ", "</span>"), "%B %d, %Y"),
            "count"        : text.remove_html(extr("Pics:", "</strong>")),
        }
