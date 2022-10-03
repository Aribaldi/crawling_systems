import argparse
import os
import sys
from common.utils import download_file
from readers.html_reader import LocalHtmlReader, RemoteHtmlReader
from readers.pdf_reader import PdfReader
from readers.word_document_reader import LocalWordReader
from extractors.html_text_extractor import HtmlTextExtractor
from extractors.pdf_text_extractor import PdfTextExtractor
from extractors.docx_text_extractor import DocxTextExtractor

format_mapping = {
    '': (RemoteHtmlReader(headers={}), HtmlTextExtractor()),
    '.html': (LocalHtmlReader(), HtmlTextExtractor()),
    '.pdf': (PdfReader(), PdfTextExtractor()),
    '.doc': (LocalWordReader(), DocxTextExtractor()),
    '.docx': (LocalWordReader(), DocxTextExtractor())
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script for parsing text from html, pdf, doc/docx formats.',
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--url',
        type=str,
        help=('url where file is stored'),
    )
    group.add_argument(
        '--path',
        type=str,
        help=('local path where file is stored'),
    )

    args = parser.parse_args()

    filepath = args.path or args.url
    _, extension = os.path.splitext(filepath)

    if args.url is not None and extension != '':
        filepath = download_file(args.url)

    if extension not in format_mapping:
        raise argparse.ArgumentError(None, 'Unsupported document type')

    reader, extractor = format_mapping[extension]

    eo = reader.read(filepath)
    text = extractor.extract(eo)

    sys.stdout.write(text)
