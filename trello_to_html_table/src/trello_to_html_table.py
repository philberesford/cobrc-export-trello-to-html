import argparse
import json
from typing import Dict, List
from pathlib import Path
import os
import re

HEADER_CELL_BACKGROUND_COLOUR = "#D6E3BC"
TABLE_STYLE ="style=\"border-collapse: collapse; border: 1px solid black;\""

def trello_to_html_table(file_path: Path):
    with open(file_path, 'r', encoding='utf-8') as file:
        raw = json.load(file)

    write_agenda(raw)
    write_horizontal_rule()
    write_actions(raw)

def write_agenda(raw: Dict[str, str]) -> None:
    html_table_values: List[List[str]] = []
    list_names = ["agenda"]
    counter = 1
    for card in get_cards_in_lists(raw, list_names):
        if not card_is_cover(card):
            title, owner = get_title_and_owner(card["name"])
            desc = card["desc"]
            html_table_values.append([f"{counter}. {title}<br />{desc}", html_strong(owner)])
            counter += 1

    html_table_headers = ["Agenda Item", "Owner(s)"]
    write_table(html_table_headers, html_table_values)


def write_actions(raw: Dict[str, str]) -> None:
    html_table_values: List[List[str]] = []
    list_names = ["closed this month", "new", "open", "on hold"]
    for card in get_cards_in_lists(raw, list_names):
        title, owner = get_title_and_owner(card["name"])
        if not card_is_cover(card):
            card_list_name = get_list_name(raw, card.get("idList"))
            desc = card["desc"]
            html_table_values.append([f"{title}<br /><br />{desc}", card_list_name, html_strong(owner)])

    html_table_headers = ["Action", "Status", "Owner(s)"]
    write_table(html_table_headers, html_table_values)


def html_strong(value: str) -> str:
    return f"<strong>{value}</strong>"


def write_horizontal_rule():
    write_html("<hr />")


def write_table(headers: List[str], values: List[List[str]]):
    write_html(f"<table width=\"100%\" cellpadding=\"9\", cellspacing=\"0\" border=\"0\" {TABLE_STYLE}>")
    write_table_headers(headers)
    write_html("<tbody>")
    for row in values:
        write_table_cells(row)
    write_html("</tbody></table>")


def write_table_cells(row: List[str]):
    write_html("<tr>")
    for cell in row:
        write_html(f"<td {TABLE_STYLE}>{cell}</td>")
    write_html("</tr>")


def write_table_headers(headers: List[str], background_colour: str = HEADER_CELL_BACKGROUND_COLOUR):
    write_html("<thead><tr>")
    for header in headers:
        write_html(f"<th align=\"left\" bgcolor=\"{background_colour}\"  {TABLE_STYLE}>{header}</th>")

    write_html("</tr> </thead>")


def write_html(s: str) -> None:
    s = s.replace("\n", "\n<br />")
    print(s, end="")


def get_title_and_owner(entry: str) -> (str, str):
    # Extract everything before the [] as the title, and everything between the [] is the owner
    values = re.findall(r'(.*)\[(.*?)\]', entry)
    title, owner = "", ""
    if len(values) > 0:
        first = values[0]
        title = first[0] if len(first) > 0 else ""
        owner = first[1] if len(first) > 1 else ""

    # If there are no 'owners' associated with the entry, then return the entry, unaltered.
    title = entry if title == "" else title
    return title, owner


def card_is_cover(card: Dict[str, str]) -> bool:
    has_uploaded_background = card.get("cover", {}).get("idUploadedBackground") is not None
    has_id_attachment = card.get("cover", {}).get("idAttachment") is not None
    return has_uploaded_background or has_id_attachment


def get_cards_in_lists(raw: Dict[str, str], list_names: List[str]) -> List[Dict[str, str]]:
    list_ids = [get_list_id(raw, list_name) for list_name in list_names]

    return [card for card in raw.get("cards", {}) if
            card_belongs_in_set_of_lists(card, list_ids) and not card_is_closed(card)]


def card_is_closed(card: Dict[str, str]) -> bool:
    card_closed = card.get("closed", False)
    return card_closed


def card_belongs_in_set_of_lists(card: Dict[str, str], list_ids: List[str]):
    card_list_id = card.get("idList", "")
    return card_list_id in list_ids


def get_list_name(raw: Dict[str, str], list_id: str) -> str:
    lists = raw.get("lists", {})
    for item in lists:
        if item.get("id") == list_id:
            return str(item.get("name", ""))

    return ""


def get_list_id(raw: Dict[str, str], list_name: str) -> str:
    lists = raw.get("lists", {})
    for item in lists:
        if str(item.get("name", "")).lower().startswith(list_name.lower()):
            return item.get("id")

    return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcePath", help='Specify the path to the export from Trello')
    args = parser.parse_args()

    path = Path(os.getcwd(), args.sourcePath)
    trello_to_html_table(path)
