from pathlib import Path
import pickle
import operator as op
import numpy as np
import json


def gamma_coding(a):
    if (a <= 0).any():
        raise ValueError("All values in a must be positive")

    a = a.view(f'u{a.itemsize}')
    l = np.log2(a).astype('u1')
    L = ((l<<1)+1).cumsum().astype(np.int64)
    out = np.zeros(L[-1],'u1')
    for i in range(l.max()+1):
        out[L-i-1] += (a>>i)&1
    return np.packbits(out), out.size


def gamma_decoding(b, n):
    b = np.unpackbits(b, count=n).view(bool)
    s = b.nonzero()[0]
    s = (s << 1).repeat(np.diff(s, prepend=-1))
    s -= np.arange(-1, len(s) - 1)
    s = s.tolist()  # list has faster __getitem__
    ns = len(s)

    def gen():
        idx = 0
        yield idx
        while idx < ns:
            idx = s[idx]
            yield idx

    offs = np.fromiter(gen(), int)
    sz = np.diff(offs) >> 1
    mx = sz.max() + 1
    out = np.zeros(offs.size - 1, int)
    for i in range(mx):
        out[b[offs[1:] - i - 1] & (sz >= i)] += 1 << i
    return out


def delta_encoding(a):
    out = np.zeros(a.shape[0])
    for i in range(a.shape[0]):
        bin_repr = np.binary_repr(num)
        bits_num = len(bin_repr)
        gamma_coded = gamma_coding(bits_num)
        out[i] = np.packbits([gamma_coded, bin_repr.tobytes()])
    return out


def zip_ind(index_path: Path, docs_path: Path, zip_index_path: Path, zip_docs_path: Path, numbered_index_path: Path, enc_type: str):

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
            ), start=1
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

    if enc_type == "gamma":
        encoded_delta_index = {
            term: gamma_coding(docs)[0].tobytes() for term, docs in diffs_index.items()
        }
    if enc_type == "delta":
        encoded_delta_index = {
            term: gamma_coding(docs)[0].tobytes() for term, docs in diffs_index.items()
        }

    with open(zip_index_path, "wb") as fp:
        pickle.dump(encoded_delta_index, fp)


if __name__ == "__main__":
    index_path = Path("./module_3/output/10000_index.pickle")
    docs_path = Path("./module_3/output/10000_docs.pickle")
    zip_index_path = Path("./module_3/output/10000_delta_index.pickle")
    zip_docs_path = Path("./module_3/output/10000_docs_zipped.pickle")
    zip_ind(index_path, docs_path, zip_index_path, zip_docs_path)
