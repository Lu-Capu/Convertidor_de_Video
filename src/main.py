import flet as ft
from ui.view import Principal


def main(page: ft.Page):
    page.title = "Descargador Multimedia"
    page.padding = 20
    page.window.width = 550
    page.window.height = 500
    page.window.min_width = 450
    page.window.min_height = 460

    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.PURPLE)
    page.bgcolor = ft.Colors.WHITE

    view = Principal(page)
    view.build_view()
    

if __name__ == "__main__":
    ft.run(main)
