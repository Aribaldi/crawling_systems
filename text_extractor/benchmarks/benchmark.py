import timeit
from pathlib import Path
from extractors.pdf_text_extractor import PdfTextExtractor
from extractors.docx_text_extractor import DocxTextExtractor
from readers.pdf_reader import PdfReader
from readers.word_document_reader import LocalWordReader
from common.text_extractor import TextExtractor
from common.document_reader import DocumentReader
import os
from functools import partial
import statistics
import pandas as pd


root = Path("./tests/benchmark/")

def read_extract(path: str, extractor: TextExtractor, reader: DocumentReader):
    temp = reader.read(str(path))
    res = extractor.extract(temp)
    return res


def time_wrapper(path, extr, reader):
    return timeit.timeit("read_extract(path, extr, reader)", 
                        number=2, 
                        globals={"read_extract": read_extract, "path": path, "extr": extr, "reader" :reader}) / 2


def folder_wrapper(folder_path, extr, reader):
    curry = partial(time_wrapper, extr=extr, reader=reader)
    full_paths = [folder_path / file_name for file_name in os.listdir(folder_path)]
    res = list(map(curry, full_paths))
    return res


def aggregate():
    res = {
        "docx" : [],
        "pdf" : []
    }

    format_mapping = {
        'docx': (LocalWordReader(), DocxTextExtractor()),
        'pdf': (PdfReader(), PdfTextExtractor())
    }

    for key in format_mapping:
        for type in ["short", "long"]:
            path = root / key / type
            reader, extr = format_mapping[key]
            res[key].append(statistics.mean(folder_wrapper(path, extr, reader)))
    res = pd.DataFrame(res)
    res["docx"] = res["docx"].apply(lambda x: f"{x // 1:.0f}s {x % 1 * 1e3:.0f}ms")
    res["pdf"] = res["pdf"].apply(lambda x: f"{x // 1:.0f}s {x % 1 * 1e3:.0f}ms")
    res.index = ["mean_short", "mean_long"]
    res.to_csv("./benchmarks/benchmark.csv")
    return res





if __name__ == "__main__":
    print(aggregate())
    #print(time_wrapper("./tests/benchmark/docx/short/5.docx", DocxTextExtractor(), LocalWordReader()))
    #print(folder_wrapper(root, PdfTextExtractor(), PdfReader()))