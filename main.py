import flet as ft 
from app import DomainsTablesApp

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = 'DomainsTablesApp'
        app = DomainsTablesApp(page)
        page.add(app.build())

    ft.app(target=main)
