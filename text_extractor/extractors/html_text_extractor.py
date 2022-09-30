from typing import Iterable
import re
from common.text_extractor import TextExtractor
from bs4 import BeautifulSoup, Tag

from extraction_objects.html_extraction_object import HtmlExtractionObject


class HtmlTextExtractor(TextExtractor):
    def __init__(self):
        super().__init__()
        self.url_pattern = r'''((?:(?<=[^a-zA-Z0-9])''' \
            r'''(?:(?:https?\:\/\/){0,1}(?:[a-zA-Z0-9\%]{1,}\:[a-zA-Z0-9\%]{1,}[@]){,1})'''\
            r'''(?:(?:\w{1,}\.{1}){1,5}(?:(?:[a-zA-Z]){1,})|'''\
            r'''(?:[a-zA-Z]{1,}\/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\:[0-9]{1,4}){1})){1}'''\
            r'''(?:(?:(?:\/{0,1}(?:[a-zA-Z0-9\-\_\=\-]){1,})*)(?:[?][a-zA-Z0-9\=\%\&\_\-]{1,}){0,1})'''\
            r'''(?:\.(?:[a-zA-Z0-9]){0,}){0,1})'''

    def extract(self, extraction_object: HtmlExtractionObject) -> str:
        soup = extraction_object.content
        extracted_text = ''
        body_tag = soup.select_one('body')

        if body_tag is not None:
            self._remove_tags(
                body_tag,
                ['image', 'table', 'code', 'header', 'footer'],
            )

            # removing <a> tags with link texts
            self._filter_link_tags(body_tag)

            extracted_text = body_tag.get_text()

            # removing links in resulting text
            extracted_text = re.sub(self.url_pattern, '', extracted_text)

            # replacing multiple spaces with only one
            extracted_text = re.sub(r'[^\S\r\n]+', ' ', extracted_text)

            # removing spaces in from of linebreaks
            extracted_text = re.sub(r'[\s]+\n', '\n', extracted_text)

        # striping all lines
        return '\n'.join([line.strip() for line in extracted_text.strip().splitlines()])

    def _filter_link_tags(self, body_tag: Tag):
        link_tags = body_tag.find_all('a')
        for link in link_tags:
            link_text = link.get_text()
            if re.search(self.url_pattern, link_text) is not None:
                link.decompose()

    def _remove_tags(self, route_tag: Tag, removing_tags: Iterable[Tag]):
        for removing_tag in removing_tags:
            found_tags = route_tag.find_all(removing_tag)
            for tag in found_tags:
                tag.decompose()
