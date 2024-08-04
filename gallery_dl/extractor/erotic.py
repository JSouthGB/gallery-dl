# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://erotic.pics/"""
import re

from .common import GalleryExtractor
from .. import text


def extract_title_data(s):
    """Extract gallery count from title."""
    pattern = re.compile(
        r"^(.*?)\s*-\s*(\d+)\s*(?:\w+.*?)?#\s*(\d+)$", flags=re.IGNORECASE)
    match = pattern.search(s)
    if match:
        return match.groups()
    else:
        return None, None, None


class EroticGalleryExtractor(GalleryExtractor):
    """Base class for Erotic extractors"""
    category = "erotic"
    root = "https://erotic.pics"
    pattern = r"(?:https?://)?erotic\.pics/([^/?#]+)"
    example = "https://erotic.pics/title-line-100-99-pics/"

    def __init__(self, match):
        self.slug = match.group(1)
        url = "{}/{}".format(self.root, self.slug)
        GalleryExtractor.__init__(self, match, url)

    def images(self, page):
        img_html = text.extr(page, '"entry themeform">', 'class="clear">')
        return ((url, None) for url in text.extract_iter(
            img_html, 'src="', '"')
                )

    def metadata(self, page):
        extr = text.extract_from(page)
        title_html = extr("<title>", "</title>")

        try:
            title, count, gallery_id = extract_title_data(title_html)
        except ValueError:
            self.log.error("Error extracting title, count, or gallery_id")
            title, count, gallery_id = "", "0", "0"  # Default values

        count = text.parse_int(count, default=0)

        date = None
        try:
            date_str = extr("</i>", "</span>")
            if date_str:
                date = text.parse_datetime(date_str, "%B %d, %Y")

        except ValueError:
            self.log.warning("Date format mismatch or date not found")

        tag = text.split_html(extr('"category tag">', "</span>"))

        data = {
            "pageurl": self.url,
            "date": date,
            "title": title,
            "gallery_id": gallery_id,
            "count": count,
            "tag": tag,
        }

        return data
