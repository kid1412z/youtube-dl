# coding: utf-8
from __future__ import unicode_literals

import re
from .common import InfoExtractor


class PlayerGlobeWienIE(InfoExtractor):
    _VALID_URL = r'https?://player.(?:globe.wien|hader.at)/(?:globe-wien|hader)/(?P<id>.*)'
    _TESTS = [
        {
            'url': 'https://player.globe.wien/globe-wien/corona-podcast-teil-4',
            'md5': 'f973a27e258bdeff686e63434e872f70',
            'info_dict': {
                'id': 'corona-podcast-teil-4',
                'ext': 'mp4',
                'title': 'Eckel & Niavarani & Sarsam - Im Endspurt versagt',
                'description': 'md5:fbd2e2a456fef3a171683dd9e33f1810',
                'thumbnail': r're:^https?://.*\.jpg',
            },
            'params': {
                'format': 'bestvideo',
                'skip_download': True,
            }
        },
        {
            'url': 'https://player.hader.at/hader/hader-indien-video',
            'md5': '0bca8d5b309361a9556cee6abff2c1b9',
            'info_dict': {
                'id': 'hader-indien-video',
                'ext': 'mp4',
                'title': 'Film der Woche - Indien',
                'description': 'md5:cad9f2bd7a0c5c0dff9cf1cff71288f6',
                'thumbnail': r're:^https?://.*\.jpg',
            },
            'params': {
                'format': 'bestvideo',
                'skip_download': True,
            }
        },
        {
            'url': 'https://player.hader.at/hader/hader-indien',
            'md5': 'b8bd7cf37d82529411a6e67005739fb3',
            'info_dict': {
                'id': 'hader-indien',
                'ext': 'mp3',
                'title': 'Hader & Dorfer lesen Indien',
                'description': 'md5:8b4e1de6c627b7d9ee6cb1c65debfa85',
                'thumbnail': r're:^https?://.*\.jpg',
            },
            'params': {
                'skip_download': True,
            }
        },
    ]

    def _real_extract(self, url):
        format_id = self._match_id(url)
        webpage = self._download_webpage(url, format_id)
        thumbnail = self._html_search_regex(
            r'<img class="(?:.+?)" src="(?P<thumbnail>.+?)"',
            webpage, 'thumbnail', group='thumbnail') or self._og_search_thumbnail(webpage)
        description = self._og_search_description(webpage)
        formats = []
        title = self._og_search_title(webpage)
        title = re.sub(r'^(Globe Wien VOD -|Hader VOD -)\s*', '', title)

        streamurl = self._download_json("https://player.globe.wien/api/playout?vodId=" + format_id,
                                        format_id).get('streamUrl')

        if streamurl.get('hls'):
            formats.extend(self._extract_m3u8_formats(
                streamurl.get('hls'), format_id, 'mp4', entry_protocol='m3u8_native', m3u8_id='hls'))

        if streamurl.get('dash'):
            formats.extend(self._extract_mpd_formats(
                streamurl.get('dash'), format_id, mpd_id='dash', fatal=False))

        if streamurl.get('audio'):
            formats.append({
                'url': streamurl.get('audio'),
                'format_id': format_id,
                'vcodec': 'none',
            })

        self._sort_formats(formats)
        return {
            'id': format_id,
            'title': title,
            'thumbnail': thumbnail,
            'description': description,
            'formats': formats,
        }
