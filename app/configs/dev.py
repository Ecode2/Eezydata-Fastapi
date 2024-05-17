"""DEV Environment"""
# mypy: ignore-errors
from typing import Annotated, Optional
from .base import Settings


class SettingsDev(Settings):
    DEBUG: Annotated[bool, True] = True
