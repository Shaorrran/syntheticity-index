import argparse
import itertools
import pathlib
import typing as tp
import string
import sys

import morpholog
import tqdm

MORPH_ENGINE = morpholog.Morpholog()


def load_words(path: pathlib.Path) -> tp.Set["str"]:
    with open(path, "r") as f:
        text = f.read()
    # TODO: stemming (ntlk or scratch?)
    words = text.split()
    return set(words)


def create_morphs(words: tp.Set["str"]) -> tp.Set["str"]:
    morphs = []
    for i in tqdm.tqdm(words):
        morphs.extend(MORPH_ENGINE.tokenize(i)) # TODO: check Morpholog fails
    morphs = list(itertools.chain(*morphs))
    return set(morphs)


def syntheticity_index(words: tp.Set["str"], morphs: tp.Set["str"]) -> float:
    if not words:
        raise ValueError("Empty text.")
    index = len(morphs) / len(words)
    if index < 1.0:
        raise ValueError("Syntheticity index less than 1. Malformed text?")
    return index


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Syntheticity index")
    argparser.add_argument("--file", dest="text_path", action="store", default=pathlib.Path("test.txt"), type=pathlib.Path, help="Load text from file")
    args = argparser.parse_args()
    if not args.text_path.expanduser().suffix == ".txt":
        print("Will not attempt to read anything other than a .txt file.", file=sys.stderr)
        exit(1)
    try:
        words = load_words(args.text_path.expanduser().resolve()) # convert to absolute, resolve symlinks and homedir
    except FileNotFoundError:
        print("No text found.", file=sys.stderr)
        exit(1)
    morphs = create_morphs(words)
    try:
        syn_index = syntheticity_index(words, morphs)
    except ValueError as e:
        print(f"{e}", file=sys.stderr)
        exit(1)
    print(f"Syntheticity index for test text: {syn_index}")
