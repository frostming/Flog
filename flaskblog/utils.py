import re


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^<>]+?>\s*(?=<[^<>]+?>)", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^<>]+?>", "", text, flags=re.DOTALL)
    return text.strip()
