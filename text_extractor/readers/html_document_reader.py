from common.document_reader import DocumentReader
import requests


class RemoteHtmlReader(DocumentReader):
    def __init__(self, headers: dict):
        super().__init__()
        self.headers = headers

    def read(self, path: str) -> str:
        return requests.get(path, headers=self.headers).text


class LocalHtmlReader(DocumentReader):
    def read(self, path: str) -> str:
        with open(path, 'r') as file:
            return file.read()
