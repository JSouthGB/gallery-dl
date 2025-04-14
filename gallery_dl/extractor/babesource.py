# -*- coding: utf-8 -*-

# Copyright 2023 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://babesource.com"""

from .common import GalleryExtractor, Message
from .. import text


class BabesourceGalleryExtractor(GalleryExtractor):
    category = "babesource"
    root = "https://babesource.com"
    directory_fmt = ("{category}", "{gallery_id}_{title}")
    archive_fmt = "{category}_{gallery_id}_{filename}"
    pattern = r"(?:https://)?babesource\.com/(galleries)/(.+)\.html"
    example = "https://babesource.com/galleries/an-album-name-123456.html"

    def __init__(self, match):
        self.slug = match.group(2)
        url = "{}/galleries/{}.html".format(self.root, self.slug)
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
        imgs = text.extr(page, 'class="box-massage__massage">', ".thumbs")
        return [
            i for i in
            text.extract_iter(imgs, '" href="', '">')
        ]

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
