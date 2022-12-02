import psycopg2
from module_2.src.storage import PostgresDB
from module_2.src.post import Post
import hashedindex
from preprocessing import clean
from collections import Counter
from joblib import Parallel, delayed
from tqdm import tqdm

Index = dict[str, dict[str, int]]


def get_texts(posts_num: int=40000):
    db = PostgresDB(
        "",
        "localhost",
        "crawling_systems",
        "iref",
        ""
    )
    posts = db.load_posts()
    return posts[:posts_num]


def single_doc_index(doc: Post):
    index = hashedindex.HashedIndex()
    for term in clean(doc.text):
        index.add_term_occurrence(term, f"{doc.post_id}, {doc.group_id}")
    return index


def global_index(documents: list[Post], p_num:int) -> tuple[Index, Counter]:
    res = Parallel(n_jobs=p_num)(
        delayed(single_doc_index)(doc) for doc in tqdm(documents, total=len(documents))
    )
    index = hashedindex.merge(res)
    all_items = {term: dict(counter) for term, counter in index.items().items()}
    return all_items, index._documents



if __name__ == "__main__":
    post = get_texts(10)
    res = global_index(post)
    print(res)
    

