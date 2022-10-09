import re
from common.extraction_object import ExtractionObject


class TextExtractor:
    def __init__(self):
        self.url_pattern = r'((?:(?<=[^a-zA-Z0-9])' \
            r'(?:(?:https?\:\/\/){0,1}(?:[a-zA-Z0-9\%]{1,}\:[a-zA-Z0-9\%]{1,}[@]){,1})'\
            r'(?:(?:\w{1,}\.{1}){1,5}(?:(?:[a-zA-Z]){1,})|'\
            r'(?:[a-zA-Z]{1,}\/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\:[0-9]{1,4}){1})){1}'\
            r'(?:(?:(?:\/{0,1}(?:[a-zA-Z0-9\-\_\=\-]){1,})*)(?:[?][a-zA-Z0-9\=\%\&\_\-]{1,}){0,1})'\
            r'(?:\.(?:[a-zA-Z0-9]){0,}){0,1})'

    def extract(self, extraction_object: ExtractionObject) -> str:
        pass

    def clean_text(self, text: str) -> str:
        # removing links in resulting text
        text = re.sub(self.url_pattern, '', text)

        # replacing multiple spaces with only one
        clean_text = re.sub(r'[^\S\r\n]+', ' ', text)

        # removing spaces in from of linebreaks
        clean_text = re.sub(r'[\s]+\n', '\n', clean_text)

        # striping all lines
        return '\n'.join([line.strip() for line in clean_text.strip().splitlines()])
