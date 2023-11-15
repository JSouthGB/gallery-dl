# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://zbporn.com/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?zbporn\.com"


class ZbpornExtractor(Extractor):
    category = 'zbporn'
    directory_fmt = ('{category}', '{title}')
    filename_fmt = '{filename}.{extension}'
    archive_fmt = '{filename}'
    # subcategory = 'gallery'
    # pattern = r'(?:https?://)?(?:www\.)?zbporn\.com'
    root = 'https://zbporn.com'
    example = 'https://zbporn.com/albums/123456/title-of-album/'


class ZbpornGalleryExtractor(ZbpornExtractor):
    subcategory = 'gallery'
    pattern = r"albums/[0-9]+/([A-Za-z0-9]+(-[A-Za-z0-9]+)+)/"

    def items(self):
        page = self.request(
            text.ensure_http_scheme(self.url)).text

        data = self.metadata(page)
        img_src = text.extr(
            page, 'gallery-holder js-album">', '</div>')
        # images = text.extract_iter(img_src, 'href="', '"')
        images = text.extract_iter(img_src, 'class="item"', 'alt="')

        yield Message.Directory, data
        tags = text.extract_iter(page, 'item-link" title="', '"')

        for count, image in enumerate(images):
            file = text.extr(images, 'href="', '"')
            width, height = text.extr(
                image, 'data-size="', '"').split(sep='x')
            img = text.nameext_from_url(image, {
                # 'num': text.parse_int(path.split('_')[-1].split('.')[0]),
                # 'date': data['date']
                'count': count,
                'pid': text.extr(image, 'data-pid="', '"'),
                'tags': list(tags),
                'width': width,
                'height': height
            })
            yield Message.Url, file, img

    def metadata(self, page):
        user_src = text.extr(page, 'icon-profile">', '</span>')
        data = {
            'pageurl': self.url,
            'title': text.extr(
                page, '<h1 class="head-row">', '</h1>'),
            'tags': text.extr(
                page, 'item-link" title="', '"'),
            'user': text.remove_html(user_src)
        }

        # data['imagecount'] = text.extr(
        #     page, '<div class="pics">', '</div>')

        # data = {k: text.unescape(data[k]) for k in data if data[k] != ""}

        return data
