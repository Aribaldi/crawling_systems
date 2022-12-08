from collections import Counter
from indexing import Index
from preprocessing import clean
from itertools import product
from typing import Callable
import operator as op
from pathlib import Path
import json
import pickle


def _get_doc_id(ids: str) -> tuple[int, int]:
    post, group = ids.split(" ")
    return int(post[:-1]), int(group)


def make_query(
    indexes: list[Index], size: int = 10
) -> Callable[[str], list[tuple[int, int]]]:
    """Create query function over indexes.

    Args:
        indexes (list[Index]): list of indexes.
        size (int, optional): query size. Defaults to 10.

    Returns:
        Callable[[str], list[tuple[int, int]]]: search function.
    """

    def query(search_query: str) -> list[tuple[int, int]]:
        query_tokens = clean(search_query)
        search_results = {token:
            Counter(index[token])
            for token, index in product(query_tokens, indexes)
            if token in index
        }
        query_terms_counters = [set(search_results[k].elements()) for k in search_results]
        intersect = set.intersection(*query_terms_counters)
        # docs_counts: dict[str, int] = dict(sum(intersect, Counter()))
        # ordered_docs = map(
        #     op.itemgetter(0),
        #     sorted(docs_counts.items(), key=op.itemgetter(1), reverse=True),
        # )

        result = list(map(_get_doc_id, intersect))
        return len(result), result[:size]

    return query

def search_wrapper(index_path: Path, search_query: str, size: int):
    if index_path.suffix == ".pickle":
        with open(index_path, "rb") as f:
            indexes = [pickle.load(f)]
    if index_path.suffix == ".json":
        indexes = [json.load(open(index_path))]
    query = make_query(indexes, size)
    docs_num, res = query(search_query)
    return docs_num, res

if __name__ == "__main__":
    res =  search_wrapper(Path("./module_3/output/10000_index.pickle"), "Ректор МГУ", 100)
    print(res)