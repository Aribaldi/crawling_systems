import argparse
from indexing import global_index, get_texts
import json
from pathlib import Path
import pickle
import time
import os

DEFAULT_SAVE_PATH = Path("./module_3")

parser = argparse.ArgumentParser(description="Wrapper for inverse index creation & query searching")
parser.add_argument("processes_num", type=int)
parser.add_argument("docs_num", type=int)
parser.add_argument("--save_path", nargs="?", type=Path, default=DEFAULT_SAVE_PATH)
parser.add_argument("--format", nargs="?", type=str, default="json")


def main(args: argparse.Namespace):
    os.makedirs(args.save_path, exist_ok=True)
    post = get_texts(args.docs_num)
    t_start = time.time()
    all_items, documents = global_index(post, args.processes_num)
    t_elapsed = time.time() - t_start
    bench_file = open(args.save_path / "bench.txt", "a+")
    bench_file.write(f"Number of docs: {args.docs_num} \t Time elapsed: {t_elapsed}\n")
    bench_file.flush()
    bench_file.close()
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
        


    


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)