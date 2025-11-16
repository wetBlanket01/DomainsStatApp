import flet as ft
from excel_data_processor import ExcelDataProcessor


class ExcelUploadField:
    def __init__(self, file_picker: ft.FilePicker, notification_container: ft.Container, on_file_loaded):
        self.file_picker = file_picker
        self.notification_container = notification_container
        self.on_file_loaded = on_file_loaded

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

    def show_message(self, message):
        self.notification_container.content = ft.Text(message, size=14, expand=True, color=ft.Colors.GREEN_400)
        self.notification_container.alignment = ft.alignment.center_left
        self.notification_container.padding = ft.padding.symmetric(horizontal=12)
        self.notification_container.visible = True

    def set_file_path(self, file):
        self.path_text.value = file.path or file.name                         

        self.path_text.color = ft.Colors.WHITE                                
        self.file_path_display.border = ft.border.all(1, ft.Colors.GREEN_400) 

    def handle_file_pick(self, e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            
            self.set_file_path(file)
            self.show_message(f'Таблица {file.name} успешно загружена!')
            
            self.on_file_loaded()
            self.file_path_display.update()
            self.notification_container.update()

            self.processor = ExcelDataProcessor(self.path_text.value)
            self.processor.process_table()
