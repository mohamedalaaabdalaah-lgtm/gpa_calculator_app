import json
import os


def load_user_data(filepath="data.json"):
    if not os.path.exists(filepath):
        default_data = {}
        save_user_data(default_data, filepath)
        return default_data

    with open(filepath, "r") as file:
        data = json.load(file)

    return data


def save_user_data(data, filepath="data.json"):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


 