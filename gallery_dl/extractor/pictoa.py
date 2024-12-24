# -*- coding: utf-8 -*-

# Copyright 2023 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://www.pictoa.com"""

from .common import GalleryExtractor, Message
from .. import text


class PictoaGalleryExtractor(GalleryExtractor):
    category = "pictoa"
    root = "https://www.pictoa.com"
    directory_fmt = ("{category}", "{gallery_id}_{title}")
    archive_fmt = "{category}_{gallery_id}_{filename}"
    pattern = r"(?:https://www)?\.pictoa\.com/(albums)/(.+)\.html"
    example = "https://www.pictoa.com.albums/an-album-name-123-1234567.html"

    def __init__(self, match):
        self.slug = match.group(2)
        url = "{}/albums/{}.html".format(self.root, self.slug)
        GalleryExtractor.__init__(self, match, url)

    def items(self):

        page = self.request(self.gallery_url).text
        imgs = self.images(page)
        data = self.metadata(page)
        data["count"] = len(imgs)

        yield Message.Directory, data

        for num, img in enumerate(imgs, start=1):
            path = text.nameext_from_url(img, {
                "num": num,
                "title": data["title"],
                "count": data["count"],
                "gallery_id": data["gallery_id"],
            })
            yield Message.Url, img, path

    def images(self, page):
        imgs = text.extr(page, '<h1>', "flagMenuFirst")
        img_list = text.extract_iter(imgs, 'data-lazy-src="', '"')
        return [i.replace("t1", "s1") for i in img_list]
        # return [i for i in text.extract_iter(
        #     imgs, 'lazy-src="', '"')]

    def metadata(self, page):
        title, gallery_id = self.get_gallery_title()
        return {
            "title": title,
            "gallery_id": gallery_id,
        }

    def get_gallery_title(self) -> tuple[str, int]:
        title, gallery_id = self.slug.rsplit("-", 1)
        title = title.replace("-", " ").title()
        gallery_id = int(gallery_id.split(".")[0])
        return title, gallery_id
