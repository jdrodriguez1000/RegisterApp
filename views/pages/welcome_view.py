import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.welcome_controller import WelcomeController
from models.welcome_model import WelcomeModel
from core.i18n import I18n

class WelcomeView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.model = WelcomeModel()
        self.controller = WelcomeController(self.model)

    def render(self):
        content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src="img/welcome_hero.png",
                            width=300,
                            height=300,
                            fit="contain",
                        ),
                        alignment=ft.Alignment(0, 0),
                        margin=ft.Margin(0, 40, 0, 20),
                    ),
                    ft.Text(
                        I18n.t("welcome.title"),
                        size=32,
                        weight="bold",
                        color="#1A1A1A",
                        text_align="center",
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        I18n.t("welcome.subtitle"),
                        size=16,
                        color="#757575",
                        text_align="center",
                    ),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.ElevatedButton(
                            content=ft.Text(
                                I18n.t("welcome.button"),
                                color="white",
                                weight="bold",
                                size=16,
                            ),
                            style=ft.ButtonStyle(
                                bgcolor="#121212",
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=ft.Padding(20, 20, 20, 20),
                            ),
                            on_click=lambda _: self.router.navigate("/register"),
                            width=float("inf"),
                        ),
                        margin=ft.Margin(0, 0, 0, 40),
                    ),
                ],
                horizontal_alignment="center",
                spacing=0,
            ),
            padding=30,
            expand=True,
            bgcolor="#F8F9FB",
        )

        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )
