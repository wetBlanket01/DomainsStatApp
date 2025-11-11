import flet as ft
from excel_upload_field import ExcelUploadField


class DomainsTablesApp:
    def __init__(self, page):
        self.page = page
        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)

        self.upload_field = ExcelUploadField(self.file_picker)
        self.upload_field2 = ExcelUploadField(self.file_picker)

    def build(self):
        return ft.Column(
            controls=[
                self.upload_field.file_path_display,
                self.upload_field2.file_path_display
            ],
            spacing=10
        )
