import json
from typing import Dict, List
from pathlib import Path
import os
import re

def trello_to_html_table(file_path: Path):
    with open(file_path, 'r', encoding='cp850') as file:
        raw = json.load(file)

    for card in get_cards_in_list(raw, "new"):
        if not card_is_cover(card):
            title, owner = get_title_and_owner(card["name"])
            desc = card["desc"]
            print(title, owner, desc)


def get_title_and_owner(entry: str) -> (str, str):
    values = re.findall(r'(.*)\[(.*?)\]', entry)
    if len(values) > 0:
        first = values [0]
        if len(first) > 0:
            title = first[0]

        if len(first) > 1:
            owner = first[1]

    return title, owner

def get_owner(entry: str):
    values = re.findall(r'\[(.*?)\]', entry)
    return ",".join(values)


def card_is_cover(card: Dict[str, str]) -> bool:
    return card.get("cover", {}).get("idAttachment") is not None


def get_cards_in_list(raw: Dict[str, str], list_name: str) -> List[Dict[str, str]]:
    target_list_id = get_list_id(raw, list_name)
    return [card for card in raw.get("cards", {}) if
            card_belongs_to_list(card, target_list_id) and not card_is_closed(card)]


def card_is_closed(card: Dict[str, str]) -> bool:
    card_closed = card.get("closed", False)
    return card_closed


def card_belongs_to_list(card: Dict[str, str], list_id: str):
    card_list_id = card.get("idList", "")
    return card_list_id == list_id


def get_list_id(raw: Dict[str, str], list_name: str) -> str:
    lists = raw.get("lists", {})
    for item in lists:
        if str(item.get("name", "")).lower().startswith(list_name.lower()):
            return item.get("id")

    return ""


if __name__ == "__main__":
    path = Path(os.getcwd(), "export.json")
    trello_to_html_table(path)
