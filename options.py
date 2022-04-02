"""Load options from file."""

import os
import json

setting_path = os.path.join(os.getcwd(), "settings.json")


def load_options(key=None):
    """Load options from file."""
    with open(setting_path, "r") as load_f:
        return json.load(load_f)[key] if key else json.load(load_f)
