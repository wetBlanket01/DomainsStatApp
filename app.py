from platform import processor
import flet as ft
from excel_upload_field import ExcelUploadField
from data_transfer_manager import DataTransferManager


class DomainsTablesApp:
    def __init__(self, page):
        self.page = page
        self.page.title = 'DomainsTablesApp'

        self.page.fonts = {
                "HackNerdFont": "https://cdn.jsdelivr.net/gh/ryanoasis/nerd-fonts@master/patched-fonts/Hack/Regular/HackNerdFont-Regular.ttf",
                }

        self.page.window.min_width = 900
        self.page.window.min_height = 700

        self.page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE, font_family="HackNerdFont")     
        self.page.theme_mode = ft.ThemeMode.DARK

        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)

        self.header_text = ft.Container(
                ft.Text('Загрузите таблицы: final_domains, Динамика сбора', size=25, font_family="HackNerdFont", no_wrap=False),
                expand=True)
        self.header_div = ft.Row([ft.Icon(ft.Icons.TABLE_VIEW, color=ft.Colors.WHITE), self.header_text], expand=True)
        
        self.download_table_button = ft.ElevatedButton(
                text="Загрузить Таблицу",
                disabled=True,
                visible=False
                )

        self.notification_container = ft.Container()
        
        self.file1_loaded = False
        self.file2_loaded = False

        self.upload_field = ExcelUploadField(file_picker=self.file_picker,
                                             notification_container=self.notification_container,
                                             on_file_loaded=lambda: self.on_file_loaded(1))
        self.upload_field2 = ExcelUploadField(file_picker=self.file_picker,
                                              notification_container=self.notification_container,
                                              on_file_loaded=lambda: self.on_file_loaded(2))
    
    def on_file_loaded(self, file_number):
        if file_number == 1:
            self.file1_loaded = True
        else:
            self.file2_loaded = True

        self.chech_both_files_loaded()

    def chech_both_files_loaded(self):
        if self.file1_loaded and self.file2_loaded:
            if self.upload_field.processor.table_name == 'final_domains':
                final_domains_data = self.upload_field.processor.table_data
                dinamic_data = self.upload_field2.processor.table_data
            else:
                final_domains_data = self.upload_field2.processor.table_data
                dinamic_data = self.upload_field.processor.table_data

            transfer_manager = DataTransferManager(final_domains=final_domains_data, dinamic=dinamic_data)

            print('chech_both_files_loaded - Success')


    def build(self):
        return ft.Column(
                controls=[ft.Container(
                    content=ft.Column(
                        controls=[
                            self.header_div,
                            self.upload_field.file_path_display,
                            self.upload_field2.file_path_display,
                            self.notification_container
                            ],
                        spacing=28,
                        ),    
                    alignment=ft.alignment.center,
                    #                    bgcolor='#22CCCC00',
                    margin=ft.margin.only(left=200,right=200, bottom=80)
                    )],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                )
