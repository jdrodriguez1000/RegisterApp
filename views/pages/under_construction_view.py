import flet as ft
from views.layouts.main_layout import MainLayout
from core.i18n import I18n

class UnderConstructionView:
    def __init__(self, page, router):
        self.page = page
        self.router = router

    def render(self):
        content = ft.Stack(
            controls=[
                # BACKGROUND
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
                            ft.Container(height=100),
                            # ICON WITH GLOW
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.CONSTRUCTION_ROUNDED,
                                    size=100,
                                    color="#1E88E5",
                                ),
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Container(height=30),
                            # TEXTS
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            I18n.t("construction.title"),
                                            size=36,
                                            weight="bold",
                                            color="#1A1A1A",
                                            text_align="center",
                                        ),
                                        ft.Container(height=15),
                                        ft.Text(
                                            I18n.t("construction.subtitle"),
                                            size=16,
                                            color="#4A4A4A",
                                            text_align="center",
                                            weight="w500",
                                        ),
                                    ],
                                    horizontal_alignment="center",
                                ),
                                padding=ft.Padding(40, 0, 40, 0),
                            ),
                            ft.Container(expand=True),
                            # BACK BUTTON
                            ft.Container(
                                content=ft.Button(
                                    content=ft.Text(
                                        I18n.t("construction.back_button"),
                                        color="white",
                                        weight="bold",
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor="#121212",
                                        shape=ft.RoundedRectangleBorder(radius=15),
                                        padding=ft.Padding(20, 20, 20, 20),
                                    ),
                                    on_click=lambda _: self.router.navigate("/login"),
                                    width=240,
                                ),
                                margin=ft.Margin(0, 0, 0, 80),
                            ),
                        ],
                        horizontal_alignment="center",
                        spacing=10,
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
