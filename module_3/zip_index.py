from pathlib import Path
import pickle
import operator as op
import numpy as np
import json

def gamma_coding(a):
    a = a.view(f'u{a.itemsize}')
    l = np.log2(a).astype('u1')
    L = ((l<<1)+1).cumsum()
    out = np.zeros(L[-1],'u1')
    for i in range(l.max()+1):
        out[L-i-1] += (a>>i)&1
    return np.packbits(out)




def zip_ind(index_path: Path, docs_path: Path, zip_index_path: Path, zip_docs_path: Path, numbered_index_path: Path):

    # def code(ids: tuple[int, str]):
    #     id, database_id = ids
    #     return gamma_coding(np.array([id])).tobytes(), database_id

    if index_path.suffix == ".pickle":
        docs_counts = pickle.load(open(docs_path, "rb"))
    if index_path.suffix == ".json":
        docs_counts = json.load(open(docs_path, "rb"))
    sorted_docs_counts = list(
        enumerate(
            map(
                op.itemgetter(0),
                sorted(docs_counts.items(), key=op.itemgetter(1), reverse=True),
            )
        )
    )
    numbered_docs = {el[1]: el[0] for el in sorted_docs_counts}
    with open(zip_docs_path, "wb") as fp:
        pickle.dump(numbered_docs, fp)

    #encoded_docs = dict(map(code, sorted_docs_counts))
    #coded_docs = {doc: code for code, doc in encoded_docs.items()}
    #with open(zip_docs_path, "wb") as fp:
        #pickle.dump(encoded_docs, fp)
    if index_path.suffix == ".pickle":
        index = pickle.load(open(index_path, "rb"))
    if index_path.suffix == ".json":
        index = json.load(open(index_path))
    # zip_index = {
    #     term: {coded_docs[doc]: count for doc, count in docs.items()}
    #     for term, docs in index.items()
    # }
    numbered_index = {
        term: {numbered_docs[doc]: count for doc, count in docs.items()}
        for term, docs in index.items()
    }

    numbered_index = {
        term: sorted(list(docs.keys())) for term, docs in numbered_index.items()
    }

    with open(numbered_index_path, "wb") as fp:
        pickle.dump(numbered_index, fp)

    diffs_index = {
        term: np.array(docs) if len(docs) == 1 else np.diff(docs) for term, docs in numbered_index.items()
    }

    encoded_delta_index = {
        term: gamma_coding(docs).tobytes() for term, docs in diffs_index.items()
    }

    with open(zip_index_path, "wb") as fp:
        pickle.dump(encoded_delta_index, fp)
    


if __name__ == "__main__":
    index_path = Path("./module_3/output/10000_index.pickle")
    docs_path = Path("./module_3/output/10000_docs.pickle")
    zip_index_path = Path("./module_3/output/10000_delta_index.pickle")
    zip_docs_path = Path("./module_3/output/10000_docs_zipped.pickle")
    zip_ind(index_path, docs_path, zip_index_path, zip_docs_path)
