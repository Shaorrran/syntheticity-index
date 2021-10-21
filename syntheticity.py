import itertools
import pathlib
import typing as tp
import string

import morpholog
import tqdm


def load_words(path: tp.Union[pathlib.Path, str]) -> tp.Set["str"]:
    if isinstance(path, str):
        path = pathlib.Path(path)
    with open(path, "r") as f:
        text = f.read()
    words = text.split()
    return set(words)


def create_morphs(words: tp.Set["str"]) -> tp.Set["str"]:
    morph_engine = morpholog.Morpholog()
    morphs = []
    for i in tqdm.tqdm(words):
        morphs.extend(morph_engine.tokenize(i))
    morphs = list(itertools.chain(*morphs))
    return set(morphs)


def syntheticity_index(words: tp.Set["str"], morphs: tp.Set["str"]) -> float:
    if not words:
        raise Exception("Empty text.")
    return len(morphs) / len(words)


if __name__ == "__main__":
    words = load_words("test.txt")
    morphs = create_morphs(words)
    syn_index = syntheticity_index(words, morphs)
    print(f"Syntheticity index for test text: {syn_index}")
