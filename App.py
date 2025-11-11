import flet as ft
from flet.utils import files

class App:
    
    def __init__(self, page: ft.Page):
        self.page = page

        self.file_picker = ft.FilePicker()

        self.page.overlay.append(self.file_picker)

        self.page.update()
