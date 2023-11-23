# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://x3vid.com/"""

from .common import GalleryExtractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?x3vid\.com"


class X3vidGalleryExtractor(GalleryExtractor):
    category = 'x3vid'
    root = 'https://x3vid.com'
    directory_fmt = ('{category}', '{title}')
    pattern = (
        BASE_PATTERN + r"/(?:gallery|gallery_pics)/(\d+)/([a-zA-Z0-9_#%]+)")
    example = 'https://x3vid.com/album-title-5-pics/'

    def __init__(self, match):
        self.gallery_id = match.group(1)
        self.title = text.unquote(match.group(2))
        url = '{}/gallery_pics/{}/{}'.format(
            self.root, self.gallery_id, self.title)
        GalleryExtractor.__init__(self, match, url)

    def images(self, page):
        url = '{}/images{{}}'.format(self.root).format
        images = text.extract_iter(page, '"/images', '"')
        return [
            (url(i), None)
            for i in images
        ]

    def metadata(self, page):
        extr = text.extract_from(page)
        return {
            'pageurl': text.unquote(self.url),
            'gallery_id': self.gallery_id,
            'title': self.title,
            'tags': text.split_html(extr('Category:', '</div>')),
        }
