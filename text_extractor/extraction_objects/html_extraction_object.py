from bs4 import BeautifulSoup
from common.extraction_object import ExtractionObject


class HtmlExtractionObject(ExtractionObject):
    def __init__(self, content: BeautifulSoup):
        super().__init__(content)
