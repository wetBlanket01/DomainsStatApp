import flet as ft
from excel_upload_field import ExcelUploadField


class DomainsTablesApp:
    def __init__(self, page):
        self.page = page
        self.page.title = 'DomainsTablesApp'
        
        self.page.fonts = {
                "HackNerdFont": "https://cdn.jsdelivr.net/gh/ryanoasis/nerd-fonts@master/patched-fonts/Hack/Regular/HackNerdFont-Regular.ttf",
                "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
                }

        self.page.window.min_width = 600
        self.page.window.min_height = 600

        self.page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE, font_family="HackNerdFont")     
        self.page.theme_mode = ft.ThemeMode.DARK

        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)

        self.header_text = ft.Container(ft.Text('Загрузите таблицы: final_domens, Динамика сбора', size=25, font_family="HackNerdFont"))
        self.header_div = ft.Row([ft.Icon(ft.Icons.TABLE_VIEW, color=ft.Colors.WHITE), self.header_text])
        
        self.upload_field = ExcelUploadField(self.file_picker)
        self.upload_field2 = ExcelUploadField(self.file_picker)

        self.notification_container = ft.Container(
                content=ft.Row([
                    ft.Text('Message Notification', color=ft.Colors.GREY_600, size=15, expand=True),
                    ft.ElevatedButton(
                        text="Загрузить Таблицу",
                        disabled=True
                        ),
                    ]),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(horizontal=12)
                ) 

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
                        spacing=30,
                        ),    
                    alignment=ft.alignment.center,
#                    bgcolor='#22CCCC00',
                    margin=ft.margin.only(left=200,right=200, bottom=80)
                    )],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                )
