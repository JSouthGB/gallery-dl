# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://x3vid.com/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?x3vid\.com"


class X3vidGalleryExtractor(Extractor):
    category = 'x3vid'
    subcategory = 'gallery'
    root = 'https://x3vid.com'
    directory_fmt = ('{category}', '{title}')
    filename_fmt = '{filename}.{extension}'
    archive_fmt = '{gallery_id}_{img_id}_{filename}'
    pattern = BASE_PATTERN + r"/gallery/(\d+)"
    example = 'https://x3vid.com/album-title-5-pics/'

    def items(self):
        page_list = [self.url]
        thumb_list = []
        page_src = self.request(
            text.ensure_http_scheme(self.url)).text

        pagination_src = text.extr(
            page_src, '"pagination"', '"next_page"')
        page_links = (
            text.extract_iter(pagination_src, 'href="', '">'))

        for page in page_links:
            page = f'{self.root}{page}'
            page_list.append(page)

        for page in page_list:
            page = self.request(page).text
            thumb_src = text.extract_iter(
                page, 'class="thumb-img">', '</a>')
            for _ in thumb_src:
                thumb_list.append(_)

        data = self.metadata(page_src)
        data['count'] = len(thumb_list)
        yield Message.Directory, data

        for num, image in enumerate(thumb_list, 1):
            rel_image = text.extr(image, 'url(/thumbs', ')"></div>')
            image_link = f'{self.root}/images{rel_image}'
            name, _, ext = image_link.rpartition(".")
            img = {
                'img_id': text.extr(image, '<img id="', '"'),
                'num': num,
                'tags': data['tags'],
                'title': data['title'],
                'count': data['count'],
                'filename': name,
                'extension': ext,
            }
            yield Message.Url, image_link, img

    def metadata(self, page):
        tag_src = text.extr(page, 'Category:', '</div>')
        data = {
            'pageurl': text.unquote(self.url),
            'gallery_id': self.url.split('/')[4],
            'title': text.extr(page, '<title>', '/title>').split(' - ')[0],
            'tags': list(text.extract_iter(tag_src, '">', '</a>'))
        }
        return data
