from bs4 import BeautifulSoup
from common.document_reader import DocumentReader
import requests
from extraction_objects.html_extraction_object import HtmlExtractionObject


class RemoteHtmlReader(DocumentReader):
    def __init__(self, headers: dict):
        super().__init__()
        self.headers = headers

    def read(self, path: str) -> HtmlExtractionObject:
        markup = requests.get(path, headers=self.headers).text
        return HtmlExtractionObject(BeautifulSoup(markup, features='html.parser'))


class LocalHtmlReader(DocumentReader):
    def read(self, path: str) -> HtmlExtractionObject:
        with open(path, 'r') as file:
            markup = file.read()
            return HtmlExtractionObject(BeautifulSoup(markup, features='html.parser'))
