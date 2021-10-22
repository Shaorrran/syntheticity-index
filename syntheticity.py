import argparse
import os
import pathlib
import string
import sys
import typing as tp

MODELS_PATH = f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}models"
os.environ["POLYGLOT_DATA_PATH"] = MODELS_PATH
# point Polyglot to models stored in the module folder

import polyglot
import polyglot.downloader
import polyglot.text
import tqdm


class LinguisticIndices:
    def __init__(
        self,
        language: tp.Optional[str] = None,
        text: tp.Optional[str] = None,
        progress: bool = True,
    ) -> None:
        self.language: tp.Optional[str] = language
        self.text: tp.Optional[str] = text
        self.text_object: tp.Optional[polyglot.text.Text] = [
            polyglot.text.Text(self.text) if self.text else None
        ]
        self.words: tp.Optional[tp.Set[str]] = None
        self.morphs: tp.Optional[tp.Set[str]] = None
        self.downloader = polyglot.downloader.Downloader(
            download_dir=f"{MODELS_PATH}{os.sep}polyglot_data"
        )
        self.progress: bool = progress

    def load_text(self, path: tp.Union[str, pathlib.Path]) -> None:
        if not path:
            raise ValueError("No path provided, can't load text.")
        if isinstance(path, str):
            path = pathlib.Path(path)
        with open(path, "r", encoding="utf-8") as text_file:
            # not supporting anything besides utf-8
            self.text = text_file.read().translate(
                str.maketrans("", "", string.punctuation)
            )
        if not self.text:
            raise ValueError("Empty text loading attempted, will not comply.")
        self.text_object = polyglot.text.Text(self.text)

    def _tokenize_into_words(self) -> None:
        if not self.text_object:
            raise ValueError("Load text using load_text() first.")
        if not self.language:
            # autodetect
            self.language = self.text_object.language.code
        self.words = {i for i in self.text_object.words}

    def _tokenize_into_morphs(self) -> None:
        morphs = []
        if not self.text_object:
            raise ValueError("Load text using load_text() first.")
        if not self.language:
            # autodetect
            self.language = self.text_object.language.code
        if not self.check_corpora_availability():
            self.download_corpora()
        if not self.words:
            self._tokenize_into_words()
        for i in tqdm.tqdm(self.words, disable=not self.progress):
            word = polyglot.text.Word(i, language=self.language)
            morphs.extend(word.morphemes)
        self.morphs = set(morphs)

    def syntheticity_index(self) -> float:
        if not self.text_object:
            raise ValueError("Load text using load_text() first.")
        if not self.words:
            self._tokenize_into_words()
        if not self.morphs:
            self._tokenize_into_morphs()
        return len(self.morphs) / len(self.words)  # type: ignore

    def check_corpora_availability(self) -> bool:
        if not self.language:
            raise ValueError("Language not set.")
        return bool(
            self.downloader.status(f"morph2.{self.language}")
            == self.downloader.INSTALLED
        )

    def download_corpora(self) -> None:
        if not self.language:
            raise ValueError("Language not set.")
        self.downloader.download(f"morph2.{self.language}")

    @property
    def language_code(self) -> str:
        if not self.language:
            raise ValueError("Language not set.")
        return self.language

    @language_code.setter
    def language_code(self, code: tp.Optional[str]) -> None:
        if not code:
            if not self.text_object:
                raise ValueError(
                    "Text required for automatic language detected, but is not loaded yet."
                )
            self.language = self.text_object.language.code
        else:
            self.language = code


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Syntheticity index")
    argparser.add_argument(
        "--file",
        dest="text_path",
        action="store",
        default=pathlib.Path(
            f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}data/test.txt"
        ),
        type=pathlib.Path,
        help="Load text from file",
    )
    args = argparser.parse_args()
    if not args.text_path.expanduser().suffix == ".txt":
        print(
            "Will not attempt to read anything other than a .txt file.", file=sys.stderr
        )
        sys.exit(1)
    indices_engine = LinguisticIndices()
    try:
        indices_engine.load_text(args.text_path.expanduser().resolve())
    except FileNotFoundError:
        print("No text found.", file=sys.stderr)
        sys.exit(1)
    try:
        syn_index = indices_engine.syntheticity_index()
    except ValueError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    print(f"Syntheticity index for test text: {syn_index}")
