"""Load and validate the settings."""

import os
import json
from pydantic import BaseModel, validator


def check_range(item: int, lb: int = None, ub: int = None):
    """Check the range of an item."""
    if lb is None:
        lb = item  # set default lower bound

    if ub is None:
        ub = item  # set default upper bound

    if item < lb or item > ub:
        raise ValueError(f'Target value {item} should be between {lb} and {ub}!')

class GameSettings(BaseModel):
    """Settings for game."""

    mode: int = 3
    height: int = 16
    width: int = 30
    mines: int = 99
    bfs: bool = False
    easy_flag: bool = False
    nf: bool = False

    @validator('height', 'width')
    def check_height_width(cls, v: int):
        """Check the range of height and width."""
        check_range(v, 1, 80)
        return v

    @validator('mines')
    def check_mines(cls, v: int, values: dict):
        """Check the range of mines."""
        # Check mine count according to width and height and maximum together
        check_range(v, 0, min(999, values['width'] * values['height'] - 1))
        return v


class UISettings(BaseModel):
    """Settings for UI."""

    skin: str = 'default'
    size: int = 32

    @validator('size')
    def check_tile_size(cls, v: int):
        """Check the range of tile size."""
        check_range(v, 10, 80)
        return v


class Settings(BaseModel):
    """Settings for all."""

    game: GameSettings = GameSettings()
    ui: UISettings = UISettings()


def load_settings() -> Settings:
    """Load settings from file."""
    SETTING_PATH = os.path.join(os.getcwd(), "settings.json")

    if not os.path.exists(SETTING_PATH):
        options = {}

    try:
        with open(SETTING_PATH, 'r', encoding='utf-8') as f:
            options = json.loads(f.read())
    except:
        options = {}

    s = Settings(**options)

    if not options:
        with open(SETTING_PATH, 'w', encoding='utf-8') as f:
            f.write(s.json(indent=4))

    return s
