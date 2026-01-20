import flet as ft
from core.theme import AppTheme

class PrimaryButton(ft.Container):
    def __init__(self, text, on_click, width=float("inf"), height=55, bgcolor=None):
        bgcolor = bgcolor or AppTheme.DEEP_BLACK
        super().__init__(
            content=ft.Button(
                content=ft.Text(
                    text,
                    color="white",
                    weight="bold",
                    size=16,
                ),
                on_click=on_click,
                style=ft.ButtonStyle(
                    bgcolor=bgcolor,
                    shape=ft.RoundedRectangleBorder(radius=AppTheme.RADIUS_SMALL),
                    padding=ft.Padding(15, 0, 15, 0),
                ),
                height=height,
            ),
            width=width,
        )
