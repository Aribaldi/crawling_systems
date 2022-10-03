from typing import Iterable
import re
from common.text_extractor import TextExtractor
from bs4 import Tag

from extraction_objects.html_extraction_object import HtmlExtractionObject


class HtmlTextExtractor(TextExtractor):
    def __init__(self):
        TextExtractor.__init__(self)

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

            extracted_text = self._clean_text(extracted_text)

        return extracted_text

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
