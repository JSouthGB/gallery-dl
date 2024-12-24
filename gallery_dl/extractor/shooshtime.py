# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://shooshtime.com/"""

from .common import GalleryExtractor
from .. import text


class ShooshtimeGalleryExtractor(GalleryExtractor):
    category = "shooshtime"
    directory_fmt = ("{category}", "{title}")
    archive_fmt = "{date}_{filename}"
    pattern = r"(?:https?://)?shooshtime.com/photos/(\d+)/([^/?#]+)"
    root = "https://shooshtime.com"
    example = "https://shooshtime.com/photos/12345/a-page-title/"

    def __init__(self, match):
        self.gallery_id = match.group(1)
        self.slug = match.group(2)
        url = "{}/photos/{}/{}".format(
            self.root, self.gallery_id, self.slug)
        GalleryExtractor.__init__(self, match, url)

    def images(self, page):
        extr = text.extr(page, 'class="album-holder">', '="info-buttons')
        return [
            (i, None) for i in
            text.extract_iter(extr, 'data-src="', '"')
        ]

    def metadata(self, page):
        return {
            "pageurl": self.url,
            "title": text.extr(
                page, '<h1 class="title">', "</h1>"),
        }
