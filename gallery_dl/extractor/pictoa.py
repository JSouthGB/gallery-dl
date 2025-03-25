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
    example = "https://www.pictoa.com/albums/an-album-name-123-1234567.html"

    def __init__(self, match):
        self.slug = match.group(2)
        url = "{}/albums/{}.html".format(self.root, self.slug)
        GalleryExtractor.__init__(self, match, url)

    @staticmethod
    def _pagination(page):
        pages = text.split_html(text.extr(
            page, '"pagination"', '</ul>'
        ))
        pnums = [int(i) for i in pages if i.isnumeric()]
        if pnums:
            return max(pnums) + 1
        return None

    def items(self):
        page = self.request(self.gallery_url).text
        imgs = self.images(page)
        data = self.metadata(page)
        pages = self._pagination(page)

        stripped_url = self.gallery_url.split('.html')[0]

        if pages is not None:
            for pnum in range(2, pages):
                page = self.request(
                    "{}-p{}.html".format(stripped_url, pnum)).text
                imgs.extend(self.images(page))

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

        cdn_prefixes = ['s1', 's2']
        valid_urls = []

        for img_url in img_list:
            for prefix in cdn_prefixes:
                full_url = img_url.replace("t1", prefix)
                try:
                    response = self.request(
                        full_url, method='HEAD', allow_redirects=False
                    )
                    if response.status_code == 200:
                        valid_urls.append(full_url)
                        break
                except Exception:
                    continue

        return valid_urls

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
