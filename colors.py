import flet as ft
from dataclasses import dataclass


@dataclass
class Colors:
    SUCCESS = ft.Colors.GREEN_400
    ERROR = ft.Colors.RED_400
    PATH_TEXT_COLOR = ft.Colors.WHITE
    SECONDARY_COLOR = ft.Colors.GREY_600
    DEFAULT_BORDER_COLOR = ft.Colors.BLUE_300
