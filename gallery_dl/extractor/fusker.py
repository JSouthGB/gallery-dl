# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://fusker.xxx/"""

from .common import GalleryExtractor
from .. import text


class FuskerGalleryExtractor(GalleryExtractor):
    category = "fusker"
    directory_fmt = ("{category}", "{title}")
    archive_fmt = "{date}_{filename}"
    pattern = r"(?:https?://)fusker\.xxx/en/([a-zA-Z0-9_#?=%&\- !()]+)"
    root = "https://fusker.xxx"
    example = "http://fusker.xxx/en/?lid=1234567&query=abcde&offset=1234"

    def __init__(self, match):
        self.lang = match.group(1)
        self.slug = match.group(2)
        url = "{}/{}/{}".format(
            self.root, self.lang, self.slug)
        GalleryExtractor.__init__(self, match, url)

    def images(self, page):
        extr = text.extr(page, '_ngcontent-serverapp-c3966829649=""', "<show-fusker")
        return [
            (self.root + i if "fusker" not in i else i, None) for i in
            text.extract_iter(extr, 'img src="', '"')
        ]

    def metadata(self, page):
        return {
            "pageurl": self.url,
            "date": text.parse_datetime(
                "{}-{}-{}".format(self.year, self.month, self.day)),
            "title": text.extr(
                page, '<h1 class="title">', "</h1>"),
            "tag": text.extr(
                page, '"><strong>', "</strong></a>"),
            "count": text.parse_int(text.extr(
                page, '<div class="pics">', "</div>")),
        }
