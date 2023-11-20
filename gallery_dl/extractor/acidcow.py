# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://acidcow.com/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r'(?:https?://)?acidcow\.com'


class AcidcowExtractor(Extractor):
    category = 'acidcow'
    root = 'http://acidcow.com'
    directory_fmt = ('{category}', '{title}')
    filename_fmt = '{title}_{filename}.{extension}'
    archive_fmt = '{date:%Y-%m-%d}_{title}_{filename}'
    pattern = r"(?:https?://)?acidcow\.com"
    example = 'https://acidcow.com/CATEGORY/TITLE-01-pics.html'

    # def parse_date(self, page_src):
    #     date = ''
    #     return date

    def items(self):
        url = self.url.strip('/')

        page_src = self.request(text.ensure_http_scheme(url)).text

        data = self.metadata(page_src)
        yield Message.Directory, data

        content = text.extr(page_src, '"newsarea">', '<p>')
        images = text.extract_iter(content, 'img src="', '"')

        for num, image in enumerate(images, start=1):
            img = text.nameext_from_url(image, {
                'num': num,
                'title': data['title'],
                'date': data['date'],
            })
            yield Message.Url, image, img

    def metadata(self, page_src):
        h1_tag = text.extr(page_src, '<h1>', '</h1>')
        infobox = text.extr(page_src, 'Category:  ', '<li><span')
        category = text.extr(infobox, 'Category:  ', '</a>')
        date = text.extr(
            infobox, '</li>\n    <li>', '&nbsp; ')
        date = text.parse_datetime(date, format='%d %b, %Y')

        data = {
            'url'     : self.url,
            'category': category,
            'title'   : h1_tag.split(' (')[0],
            'count'   : text.extr(h1_tag, ' (', ' '),
            'date'    : date
        }
        return data

