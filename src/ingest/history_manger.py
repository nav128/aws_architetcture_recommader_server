import json
from typing import TypedDict, Set

class HistoryState(TypedDict):
    page: int
    visited_repos: Set[str]

def save_state(page, visited_repos):
    with open("repo_state.json", "w") as f:
        json.dump({"page": page, "visited_repos": visited_repos}, f)

def load_state() -> HistoryState :
    try:
        with open("repo_state.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"page": 0, "visited_repos": []}

