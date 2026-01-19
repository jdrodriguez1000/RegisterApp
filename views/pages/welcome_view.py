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
        content = ft.Stack(
            controls=[
                # BACKGROUND IMAGE
                ft.Image(
                    src="img/welcome_bg.png",
                    width=390,
                    height=844,
                    fit="cover",
                ),
                # CONTENT OVERLAY
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(expand=True),
                            # TEXT AREA WITH GLASSMORPHISM FEEL
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "RegisterApp",
                                            size=44,
                                            weight="bold",
                                            color="#1A1A1A",
                                            text_align="center",
                                        ),
                                        ft.Container(height=10),
                                        ft.Text(
                                            I18n.t("welcome.subtitle"),
                                            size=18,
                                            color="#4A4A4A",
                                            text_align="center",
                                            weight="w500",
                                        ),
                                    ],
                                    horizontal_alignment="center",
                                ),
                                padding=ft.Padding(20, 0, 20, 0),
                            ),
                            ft.Container(expand=True),
                            # BUTTON AREA
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Text(
                                        I18n.t("welcome.button"),
                                        color="white",
                                        weight="bold",
                                        size=18,
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor="#121212",
                                        shape=ft.RoundedRectangleBorder(radius=15),
                                        padding=ft.Padding(25, 25, 25, 25),
                                    ),
                                    on_click=lambda _: self.router.navigate("/register"),
                                    width=float("inf"),
                                ),
                                margin=ft.Margin(30, 0, 30, 60),
                            ),
                        ],
                        horizontal_alignment="center",
                        spacing=0,
                    ),
                    expand=True,
                ),
            ],
            expand=True,
        )

        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
            show_app_bar=False,
            show_bottom_bar=False,
        )
