import flet as ft 
from App import App

if __name__ == "__main__":

    def main(page: ft.Page):

        page.title = "DomainsTablesApp"
        page.padding = 0
        
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        btn = ft.ElevatedButton("Choose files...",
                          on_click=lambda _: file_picker.pick_files(allow_multiple=True))
        
        page.add(btn)

        page.update()

    ft.app(main)
