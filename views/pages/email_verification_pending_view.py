import flet as ft
from views.layouts.main_layout import MainLayout
from core.i18n import I18n

class EmailVerificationPendingView:
    def __init__(self, page, router):
        self.page = page
        self.router = router

    def render(self):
        # Force Light Mode for consistent card rendering
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.update()

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
                            ft.Container(height=60),
                            # Header Title
                            ft.Text(
                                "RegisterApp",
                                size=32,
                                weight="bold",
                                color="#1A1A1A",
                            ),
                            ft.Container(height=30),
                            # WHITE CARD CONTAINER
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        # VERIFICATION ICON
                                        ft.Container(
                                            content=ft.Icon(
                                                ft.Icons.MARK_EMAIL_READ_OUTLINED,
                                                size=80,
                                                color="#1E88E5",
                                            ),
                                            alignment=ft.Alignment(0, 0),
                                        ),
                                        ft.Container(height=20),
                                        # TEXTS
                                        ft.Text(
                                            I18n.t("verification.title"),
                                            size=26,
                                            weight="bold",
                                            color="#1A1A1A",
                                            text_align="center",
                                        ),
                                        ft.Container(height=10),
                                        ft.Text(
                                            I18n.t("verification.subtitle"),
                                            size=15,
                                            color="#4A4A4A",
                                            text_align="center",
                                            weight="w500",
                                        ),
                                        ft.Container(height=30),
                                        # ACTIONS
                                        ft.Button(
                                            content=ft.Text(
                                                I18n.t("verification.check_button"),
                                                color="white",
                                                weight="bold",
                                            ),
                                            style=ft.ButtonStyle(
                                                bgcolor="#121212",
                                                shape=ft.RoundedRectangleBorder(radius=12),
                                                padding=ft.Padding(20, 20, 20, 20),
                                            ),
                                            on_click=lambda _: self.router.navigate("/login"),
                                            width=float("inf"),
                                        ),
                                        ft.Container(height=15),
                                        # Resend Link (Darker/Black for contrast inside card)
                                        ft.TextButton(
                                            content=ft.Text(
                                                I18n.t("verification.resend_link"),
                                                color="#1E88E5", # Keeps branding, readable on white
                                                weight="bold", 
                                                size=14,
                                            ),
                                            on_click=lambda _: print("Resend email logic..."),
                                        ),
                                        # Back to Home (Dark grey/Black)
                                        ft.TextButton(
                                            content=ft.Text(
                                                I18n.t("verification.back_to_login"),
                                                color="#1A1A1A", # Darker as requested
                                                size=14,
                                                weight="bold"
                                            ),
                                            on_click=lambda _: self.router.navigate("/login"),
                                        ),
                                    ],
                                    horizontal_alignment="center",
                                    spacing=5,
                                ),
                                bgcolor="white",
                                padding=ft.Padding(30, 40, 30, 30),
                                border_radius=24,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=15,
                                    color=ft.Colors.with_opacity(0.1, "black"),
                                    offset=ft.Offset(0, 5),
                                ),
                                margin=ft.Margin(20, 0, 20, 0),
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
