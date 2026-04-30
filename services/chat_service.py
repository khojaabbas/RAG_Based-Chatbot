import os
import json

from config.settings import CHAT_DIR


def load_chat(chat_id):
    path = os.path.join(CHAT_DIR, f"{chat_id}.json")

    if not os.path.exists(path):
        data = {
            "title": "New Chat",
            "collection": None,
            "messages": []
        }
        save_chat(chat_id, data)
        return data

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_chat(chat_id, data):
    path = os.path.join(CHAT_DIR, f"{chat_id}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def delete_chat(chat_id):
    path = os.path.join(CHAT_DIR, f"{chat_id}.json")

    if os.path.exists(path):
        os.remove(path)


def get_all_chats():
    chats = []

    for file in os.listdir(CHAT_DIR):
        if file.endswith(".json"):
            chat_id = file.replace(".json", "")
            data = load_chat(chat_id)
            chats.append((chat_id, data.get("title", "Untitled Chat")))

    return chats