import re
import string
import operator as op
import pymorphy2
from toolz import compose


def remove_punct(text: str) -> str:
    return re.sub(r"[^a-zA-Zа-яА-ЯЁё0-9 ]", " ", text)


def tokenize(text: str, sep: str = " ") -> list[str]:
    return list(filter(lambda x:x != '', text.replace("\n", " ").split(sep)))


def lemmatize(tokens: list[str]) -> list[str]:
    morph = pymorphy2.MorphAnalyzer()
    return list(
        map(
            compose(
                op.attrgetter("normal_form"),
                op.itemgetter(0),
                morph.parse,
            ),
            tokens,
        )
    )


def clean(text: str) -> list[str]:
    return compose(
        lemmatize,
        tokenize,
        remove_punct,
        str.lower,
    )(text)
