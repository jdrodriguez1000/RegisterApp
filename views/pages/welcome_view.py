import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.welcome_controller import WelcomeController
from models.welcome_model import WelcomeModel
from core.i18n import I18n
from views.components.primary_button import PrimaryButton

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
                                            size=54,
                                            weight="bold",
                                            color="#1A1A1A",
                                            text_align="center",
                                        ),
                                        ft.Container(height=15),
                                        ft.Text(
                                            I18n.t("welcome.subtitle"),
                                            size=18,
                                            color="#333333",
                                            text_align="center",
                                            weight="w400",
                                            italic=True,
                                        ),
                                    ],
                                    horizontal_alignment="center",
                                ),
                                padding=ft.Padding(20, 0, 20, 0),
                            ),
                            ft.Container(expand=True),
                            # BUTTON AREA
                            ft.Container(
                                content=PrimaryButton(
                                    text=I18n.t("welcome.button"),
                                    on_click=lambda _: self.router.navigate("/login")
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
