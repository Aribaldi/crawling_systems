import argparse
from indexing import global_index, get_texts
import json
from pathlib import Path
import pickle
import time
import os
from search import search_wrapper
from zip_index import zip_ind
import os

DEFAULT_SAVE_PATH = Path("./module_3")

parser = argparse.ArgumentParser(description="Wrapper for inverse index creation & query searching")
parser.add_argument("processes_num", type=int)
parser.add_argument("docs_num", type=int)
parser.add_argument("query", type=str)
parser.add_argument("--save_path", nargs="?", type=Path, default=DEFAULT_SAVE_PATH)
parser.add_argument("--format", nargs="?", type=str, default="json")
parser.add_argument("--format", nargs="?", type=str, default="gamma")


def main(args: argparse.Namespace):
    print(args.query)
    os.makedirs(args.save_path, exist_ok=True)
    post = get_texts(args.docs_num)
    t_start = time.time()
    all_items, documents = global_index(post, args.processes_num)
    t_elapsed = time.time() - t_start
    bench_file = open(args.save_path / "bench.txt", "a+")
    bench_file.write(f"INDEX: Number of docs: {args.docs_num} \t Time elapsed: {t_elapsed}\n")
    

    if args.format == "json":
        with open(args.save_path / f"{args.docs_num}_index.json", "w") as fp:
            json.dump(all_items, fp)
        with open(args.save_path / f"{args.docs_num}_docs.json", "w") as fp:
            json.dump(dict(documents), fp)
    elif args.format == "pickle":
        with open(args.save_path / f"{args.docs_num}_index.pickle", 'wb') as fp:
            pickle.dump(all_items, fp)
        with open(args.save_path / f"{args.docs_num}_docs.pickle", 'wb') as fp:
            pickle.dump(documents, fp)

    t_start = time.time()
    if args.format == "json":
        docs_num, found_posts = search_wrapper(args.save_path / f"{args.docs_num}_index.json", args.query, 10)
    elif args.format == "pickle":
        docs_num, found_posts = search_wrapper(args.save_path / f"{args.docs_num}_index.pickle", args.query, 10)
    t_elapsed = time.time() - t_start

    bench_file.write(f"SEARCH: Number of docs with query '{args.query}': {docs_num} \t Time elapsed: {t_elapsed}\n")

    t_start = time.time()
    if args.format == "json":
        orignal_size = os.path.getsize(args.save_path / f"{args.docs_num}_index.json") / 1024 / 1024
        zip_ind(
            args.save_path / f"{args.docs_num}_index.json", 
            args.save_path / f"{args.docs_num}_docs.json", 
            args.save_path / f"{args.docs_num}_delta_index.pickle",
            args.save_path / f"{args.docs_num}_docs_zipped.pickle",
            args.save_path / f"{args.docs_num}_numbered_index.pickle",
            args.enc_type
        )
    elif args.format == "pickle":
        orignal_size = os.path.getsize(args.save_path / f"{args.docs_num}_index.pickle") / 1024 / 1024
        zip_ind(
            args.save_path / f"{args.docs_num}_index.pickle", 
            args.save_path / f"{args.docs_num}_docs.pickle", 
            args.save_path / f"{args.docs_num}_delta_index.pickle",
            args.save_path / f"{args.docs_num}_docs_zipped.pickle",
            args.save_path / f"{args.docs_num}_numbered_index.pickle",
            args.enc_type
        )
    zipped_size = os.path.getsize(args.save_path / f"{args.docs_num}_delta_index.pickle") / 1024 / 1024
    numbered_size = os.path.getsize(args.save_path / f"{args.docs_num}_numbered_index.pickle") / 1024 / 1024


    t_elapsed = time.time() - t_start


    bench_file.write(f"ZIP: Number of docs: {args.docs_num} \t Time elapsed: {t_elapsed}\
    Original index size: {orignal_size} \t Numbered indexed size: {numbered_size}\
    Zipped index size: {zipped_size} \n")
    bench_file.write("#"*128)
    bench_file.write("\n")
    bench_file.flush()
    bench_file.close()
    

    


    


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)