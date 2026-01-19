import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.login_controller import LoginController
from models.login_model import LoginModel
from core.i18n import I18n

class LoginView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.model = LoginModel()
        self.controller = LoginController(self.model)
        
        # UI controls that need references
        self.email_input = ft.TextField(
            label=I18n.t("login.email_label"),
            hint_text="example@email.com",
            bgcolor="white",
            border_radius=12,
            border_color="#E0E0E0",
            focused_border_color="#121212",
            color="#1A1A1A",
            label_style=ft.TextStyle(color="#2D2D2D"),
            hint_style=ft.TextStyle(color="#BCBCBC"),
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            keyboard_type=ft.KeyboardType.EMAIL,
        )
        
        self.password_input = ft.TextField(
            label=I18n.t("login.password_label"),
            password=True,
            can_reveal_password=True,
            bgcolor="white",
            border_radius=12,
            border_color="#E0E0E0",
            focused_border_color="#121212",
            color="#1A1A1A",
            label_style=ft.TextStyle(color="#2D2D2D"),
            hint_style=ft.TextStyle(color="#BCBCBC"),
            prefix_icon=ft.Icons.LOCK_OUTLINED,
        )
        
        self.error_text = ft.Text("", color="red", size=14, text_align="center")

    async def _on_login_click(self, e):
        success = await self.controller.handle_login(
            self.email_input.value,
            self.password_input.value,
            self.page,
            self.router
        )
        if success:
            self.router.navigate("/dashboard")
        else:
            self.error_text.value = self.model.error_message
            self.page.update()

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
                # FORM CONTAINER
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=80),
                            # Header
                            ft.Text(
                                "RegisterApp",
                                size=32,
                                weight="bold",
                                color="#1A1A1A",
                            ),
                            ft.Container(height=40),
                            # Login Card
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            I18n.t("login.title"),
                                            size=24,
                                            weight="bold",
                                            color="#1A1A1A",
                                        ),
                                        ft.Text(
                                            I18n.t("login.subtitle"),
                                            size=14,
                                            color="#2D2D2D", # Mas oscuro
                                        ),
                                        ft.Container(height=20),
                                        self.email_input,
                                        ft.Container(height=10),
                                        self.password_input,
                                        ft.Container(
                                            content=ft.TextButton(
                                                I18n.t("login.forgot_password"),
                                                style=ft.ButtonStyle(color="#444444"), # Mas oscuro
                                            ),
                                            alignment=ft.Alignment(1, 0),
                                        ),
                                        ft.Container(height=10),
                                        self.error_text,
                                        ft.Container(height=10),
                                        # Login Button
                                        ft.ElevatedButton(
                                            content=ft.Text(
                                                I18n.t("login.login_button"),
                                                color="white",
                                                weight="bold",
                                                size=16,
                                            ),
                                            style=ft.ButtonStyle(
                                                bgcolor="#121212",
                                                shape=ft.RoundedRectangleBorder(radius=12),
                                                padding=ft.Padding(20, 20, 20, 20),
                                            ),
                                            on_click=self._on_login_click,
                                            width=float("inf"),
                                        ),
                                        ft.Container(height=20),
                                        # Footer Link
                                        ft.Row(
                                            controls=[
                                                ft.Text(I18n.t("login.no_account"), color="#2D2D2D"), # Mas oscuro
                                                ft.TextButton(
                                                    I18n.t("login.join_us"),
                                                    on_click=lambda _: self.router.navigate("/register"),
                                                ),
                                            ],
                                            alignment="center",
                                        ),
                                    ],
                                    spacing=0,
                                ),
                                bgcolor="white", # Opaco para contraste
                                padding=ft.Padding(30, 30, 30, 30),
                                border_radius=24,
                                # Sombra para resaltar
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
