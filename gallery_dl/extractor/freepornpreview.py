# # -*- coding: utf-8 -*-
#
# # This program is free software; you can redistribute it and/or modify
# # it under the terms of the GNU General Public License version 2 as
# # published by the Free Software Foundation.
#
# """
# Extractors for https://freepornpreview.net/
# This only works on the 'tumblr' subdomain
# """
#
# from .common import GalleryExtractor
# from .. import text
#
#
# class FreepornpreviewGalleryExtractor(GalleryExtractor):
#     category = "erooups"
#     directory_fmt = ("{category}", "{title}")
#     archive_fmt = "{date}_{filename}"
#     pattern = r"(?:https?://)(?:(\w+)\.)?freepornpreview\.net/?(.*)"
#     root = "https://freepornpreview.net"
#     example = "https://tumblr.freepornpreview.net/chivuron/post/116983934077/"
#
#     def __init__(self, match):
#         self.subdomain = match.group(1)
#         self.slug = match.group(2)
#         url = "https://{}.freepornpreview.net/{}".format(
#             self.subdomain, self.slug)
#         GalleryExtractor.__init__(self, match, url)
#
#     def images(self, page):
#         extr = text.extr(page, )
