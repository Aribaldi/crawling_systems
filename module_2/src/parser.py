import re
from typing import Dict

from src.post import Post

FIELD_KEYS = ["id", "owner_id", "from_id", "date", "text", "comment", "likes", "reposts", "views"]


def preprocess_text(text):
    text = text.lower()
    text = re.sub("ё", "е", text)
    text = re.sub(r"\[[^\[\]|]+\|([A-Za-zа-яА-я\d ]+)]", "\1", text)
    text = re.sub(r"(https:\/\/|http:\/\/|www.)([\w.\/\-\?\&\=])+", " ", text)
    text = re.sub(r"[^A-Za-zА-Яа-я\d!\"\',:;%\-\.\?\*\(\)\/ ]", " ", text)
    return text.strip()


def select_fields(post_dict):
    if all(key in post_dict for key in FIELD_KEYS):
        return Post(
            post_id=post_dict["id"],
            group_id=post_dict["owner_id"],
            publisher_id=post_dict["from_id"],
            date=post_dict["date"],
            text=post_dict["text"],
            comments=post_dict["comments"]["count"],
            likes=post_dict["likes"]["count"],
            reposts=post_dict["reposts"]["count"],
            views=post_dict["views"]["count"],
        )
    else:
        return None


class Parser:
    def __init__(self, filter_words):
        self.filter_words = filter_words

    def parse(self, post_dict: Dict):
        post = select_fields(post_dict)
        if post is not None:
            post.text = preprocess_text(post.text)
            if any(word in post.text for word in self.filter_words):
                return post
        else:
            return None
