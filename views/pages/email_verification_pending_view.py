import flet as ft
from views.layouts.main_layout import MainLayout
from core.i18n import I18n

class EmailVerificationPendingView:
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
                            # VERIFICATION ICON
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.MARK_EMAIL_READ_OUTLINED,
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
                                            I18n.t("verification.title"),
                                            size=32,
                                            weight="bold",
                                            color="#1A1A1A",
                                            text_align="center",
                                        ),
                                        ft.Container(height=15),
                                        ft.Text(
                                            I18n.t("verification.subtitle"),
                                            size=16,
                                            color="#121212",
                                            text_align="center",
                                            weight="w500",
                                        ),
                                    ],
                                    horizontal_alignment="center",
                                ),
                                padding=ft.Padding(40, 0, 40, 0),
                            ),
                            ft.Container(expand=True),
                            # ACTIONS
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Button(
                                            content=ft.Text(
                                                I18n.t("verification.check_button"),
                                                color="white",
                                                weight="bold",
                                            ),
                                            style=ft.ButtonStyle(
                                                bgcolor="#121212",
                                                shape=ft.RoundedRectangleBorder(radius=15),
                                                padding=ft.Padding(20, 20, 20, 20),
                                            ),
                                            on_click=lambda _: self.router.navigate("/login"),
                                            width=float("inf"),
                                        ),
                                        ft.TextButton(
                                            content=ft.Text(
                                                I18n.t("verification.resend_link"),
                                                color="#1E88E5",
                                                weight="bold",
                                                size=14,
                                            ),
                                            on_click=lambda _: print("Resend email logic..."),
                                        ),
                                        ft.TextButton(
                                            content=ft.Text(
                                                I18n.t("verification.back_to_login"),
                                                color="#444444",
                                                size=14,
                                            ),
                                            on_click=lambda _: self.router.navigate("/login"),
                                        ),
                                    ],
                                    horizontal_alignment="center",
                                    spacing=10,
                                ),
                                margin=ft.Margin(30, 0, 30, 40),
                            ),
                        ],
                        horizontal_alignment="center",
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
