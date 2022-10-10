from docx import Document
from readers.html_reader import RemoteHtmlReader
from extractors.html_text_extractor import HtmlTextExtractor
from pathlib import Path
from functools import partial
import os

root_path = Path("./tests/benchmark")
docx_path = root_path / "docx"
pdf_path = root_path / "pdf"

def save_docx(url: str, output_path : Path):
    html_extr = HtmlTextExtractor()
    remote_reader = RemoteHtmlReader(headers={})
    html_obj = remote_reader.read(url)
    test_text = html_extr.extract(html_obj)
    doc = Document()
    doc.add_paragraph(test_text)
    file_list = sorted(os.listdir(output_path))
    if file_list:
        filename = str(int(file_list[-1][:-5]) + 1)
    else:
        filename = "1"
    doc.save(output_path /  f"{filename}.docx")



def save_articles():
    links_dict = {
        "short": [
            "https://ru.wikipedia.org/wiki/%D0%90%D0%B1%D1%81%D1%82%D1%80%D0%B0%D0%BA%D1%82%D0%BD%D1%8B%D0%B9_%D1%82%D0%B8%D0%BF_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85",
            "https://ru.wikipedia.org/wiki/%D0%90%D0%B2%D1%82%D0%BE%D0%BD%D0%BE%D0%BC%D0%BD%D1%8B%D0%B5_%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D1%81%D1%82%D0%B0%D0%BD%D1%86%D0%B8%D0%B8",
            "https://ru.wikipedia.org/wiki/%D0%90%D0%BA%D0%B2%D0%B8%D0%BB%D0%B8%D0%B9",
            "https://ru.wikipedia.org/wiki/%D0%90%D0%B2%D1%82%D0%BE%D0%BB%D0%B0%D0%B2%D0%BA%D0%B0",
            "https://ru.wikipedia.org/wiki/%D0%90%D0%B4%D0%B0%D0%BF%D1%82%D0%BE%D0%BC%D0%B5%D1%82%D1%80"
        ],
        "long": [
            "https://ru.wikipedia.org/wiki/%D0%A5%D1%80%D0%BE%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F_%D0%92%D0%B8%D0%B7%D0%B0%D0%BD%D1%82%D0%B8%D0%B8",
            "https://ru.wikipedia.org/wiki/%D0%90%D0%B2%D0%B3%D1%83%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%BF%D1%83%D1%82%D1%87",
            "https://ru.wikipedia.org/wiki/%D0%A1%D0%B0%D0%B5%D0%BD%D1%82%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F",
            "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BE%D0%BA%D1%80%D1%83%D0%B3%D0%BE%D0%B2_%D0%A1%D0%A8%D0%90",
            "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D0%BE%D1%80%D0%BE%D0%B4_%D0%BA%D0%BE%D0%B7"
        ]
    }
    for key in links_dict:
        out_path = docx_path / key
        curry_path = partial(save_docx, output_path=out_path)
        list(map(curry_path, links_dict[key]))


def convert_to_pdf():
    for type in ["short", "long"]:
        for file in os.listdir(docx_path / type):
            inp = docx_path / type / file
            out = pdf_path / type
            os.system(f"lowriter --convert-to pdf {inp} --outdir {out}")


if __name__ == "__main__":
    save_articles()
    convert_to_pdf()
