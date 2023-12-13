# -*- coding: utf-8 -*-

# Copyright 2023 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://x3vid.com/"""

from .common import GalleryExtractor, Message
from .. import text


class X3vidGalleryExtractor(GalleryExtractor):
    category = "x3vid"
    root = "https://x3vid.com"
    directory_fmt = ("{category}", "{title}")
    pattern = (r"(?:https?://)?x3vid\.com/"
               r"(?:gallery|gallery_pics)/(\d+)/([a-zA-Z0-9_#?=%\- ]+)")
    example = "https://x3vid.com/gallery/12345678/album-title-5-pics/"

    def __init__(self, match):
        self.gallery_id = match.group(1)
        self.title = match.group(2)
        url = "{}/gallery_pics/{}/{}".format(
            self.root, self.gallery_id, self.title)
        GalleryExtractor.__init__(self, match, url)

    @staticmethod
    def pagination(page):
        pages = text.split_html(text.extr(
            page, 'class="pagination"', "</div>"))
        pnums = [int(i) for i in pages if i.isnumeric()]
        return max(pnums)

    def items(self):
        page = self.request(self.gallery_url).text
        imgs = self.images(page)
        data = self.metadata(page)

        for pnum in range(2, self.pagination(page) + 1):
            page = self.request(
                "{}?page={}&root=1".format(self.gallery_url, pnum)).text
            images = self.images(page)
            imgs.extend(images)

        data["count"] = len(imgs)

        yield Message.Directory, data
        for num, img in enumerate(imgs, start=1):
            path = text.nameext_from_url(img, {
                "num": num,
                "title": data["title"],
                "gallery_id": self.gallery_id,
                "count": data["count"]
            })
            yield Message.Url, img, path

    def images(self, page):
        imgs = text.extr(page, 'main-content">', "</body>")
        return [self.root + i for i in text.extract_iter(
            imgs, 'src="', '"')]

    def metadata(self, page):
        extr = text.extract_from(page)
        return {
            "pageurl": text.unquote(self.url),
            "gallery_id": self.gallery_id,
            "title": text.unquote(self.title),
            "tags": text.split_html(extr("Category:", "</div>")),
        }
