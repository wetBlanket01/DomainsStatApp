import flet as ft


class ExcelUploadField:
    def __init__(self, file_picker: ft.FilePicker):
        self.file_picker = file_picker

        self.path_text = ft.Text(
                "Файл не выбран",
                color=ft.Colors.GREY_600,
                size=14,
                expand=True
                )

        self.select_button = ft.ElevatedButton(
                text="Выбрать файл",
                on_click=self.pick_file
                )

        self.file_path_display = ft.Container(
                content=ft.Row([
                    self.path_text,
                    self.select_button
                    ],
                               vertical_alignment=ft.CrossAxisAlignment.CENTER,
                               ),
                padding=12,
                border=ft.border.all(1.1, ft.Colors.BLUE_300),
                border_radius=15,
                )

    def pick_file(self, e):
        self.file_picker.on_result = self.handle_file_pick
        self.file_picker.pick_files(allow_multiple=False, allowed_extensions=['csv', 'xls', 'xlsx'])

    def handle_file_pick(self, e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            self.path_text.value = file.path or file.name
            self.path_text.color = ft.Colors.WHITE
            self.file_path_display.border = ft.border.all(1, ft.Colors.GREEN_400)
            self.file_path_display.update()
