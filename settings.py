"""Load and validate the settings."""

import os
import json
from pydantic import BaseSettings, validator


def check_range(item: int, lb: int = None, ub: int = None) -> bool:
    """Check the range of an item."""
    if lb is None:
        lb = item  # set default lower bound

    if ub is None:
        ub = item  # set default upper bound

    try:
        return lb <= item <= ub
    except:
        return False


class GameSettings(BaseSettings):
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
        if not check_range(v, 1, 80):
            raise ValueError('Height and width should be between 1 and 80!')
        return v

    @validator('mines')
    def check_mines(cls, v: int):
        """Check the range of mines."""
        if not check_range(v, 0, 999):
            raise ValueError('Mines should be between 0 and 999!')
        return v


class UISettings(BaseSettings):
    """Settings for UI."""

    skin: str = 'default'
    size: int = 32

    @validator('size')
    def check_tile_size(cls, v: int):
        """Check the range of tile size."""
        if not check_range(v, 10, 80):
            raise ValueError('Size of a tile shoule be between 10 and 80!')
        return v


class Settings(BaseSettings):
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
