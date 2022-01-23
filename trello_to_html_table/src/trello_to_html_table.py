import json
from typing import Dict, List
from pathlib import Path
import os


def trello_to_html_table(file_path: Path):
    with open(file_path, 'r', encoding='cp850') as file:
        raw = json.load(file)

    for card in get_cards_in_list(raw, "Agenda"):
        if not card_is_cover(card):
            print(card["name"], card["desc"])


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
        if str(item.get("name", "")).startswith(list_name):
            return item.get("id")

    return ""


if __name__ == "__main__":
    path = Path(os.getcwd(), "export.json")
    trello_to_html_table(path)
