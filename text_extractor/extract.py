import argparse
import os
import sys
from common.utils import download_file
from readers.html_reader import LocalHtmlReader
from readers.pdf_reader import PdfReader
from extractors.html_text_extractor import HtmlTextExtractor
from extractors.pdf_text_extractor import PdfTextExtractor

format_mapping = {
    '.html': (LocalHtmlReader(), HtmlTextExtractor()),
    '.pdf': (PdfReader(), PdfTextExtractor()),
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script for parsing text from various document formats.',
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
        help=('path where file is stored'),
    )

    args = parser.parse_args()

    if args.url is not None:
        filepath = download_file(args.url)
    else:
        filepath = args.path

    _, extension = os.path.splitext(filepath)
    if extension not in format_mapping.keys():
        raise argparse.ArgumentError(None, 'Unsupported document type')

    reader, extractor = format_mapping[extension]

    eo = reader.read(filepath)
    text = extractor.extract(eo)

    sys.stdout.write(text)
