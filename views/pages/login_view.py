import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.login_controller import LoginController
from models.login_model import LoginModel
from core.i18n import I18n
from views.components.custom_text_field import CustomTextField
from views.components.primary_button import PrimaryButton
from views.components.custom_snackbar import CustomSnackbar

class LoginView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.model = LoginModel()
        self.controller = LoginController(self.model)
        
        # UI controls that need references
        self.email_input = CustomTextField(
            label=I18n.t("login.email_label"),
            hint_text="example@email.com",
            icon=ft.Icons.EMAIL_OUTLINED,
            keyboard_type=ft.KeyboardType.EMAIL,
        )
        
        self.password_input = CustomTextField(
            label=I18n.t("login.password_label"),
            password=True,
            can_reveal_password=True,
            icon=ft.Icons.LOCK_OUTLINED,
        )
        
        # Custom Shared Components
        self.snack = CustomSnackbar()
        self.login_button = PrimaryButton(
            text=I18n.t("login.login_button"),
            on_click=self._on_login_click
        )

    async def _on_login_click(self, e):
        route = await self.controller.handle_login(
            self.email_input.value,
            self.password_input.value,
            self.page,
            self.router
        )
        if route:
            self.router.navigate(route)
        else:
            await self.snack.show(self.controller.model.error_message or "Error desconocido")

    def render(self):
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = None # Reset theme to default to avoid artifacts from other views
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
                                            size=12, # Reducido un punto más
                                            color="#1A1A1A",
                                            weight="w500",
                                        ),
                                        ft.Container(height=20),
                                        self.email_input,
                                        ft.Container(height=10),
                                        self.password_input,
                                        ft.Container(
                                            content=ft.TextButton(
                                                content=ft.Text(
                                                    I18n.t("login.forgot_password"),
                                                    color="#1E88E5",
                                                    size=13, # Tamaño ajustado
                                                    weight="bold", # Mismo formato que Unete a nosotros
                                                ),
                                                on_click=lambda _: self.router.navigate("/construction"),
                                            ),
                                            alignment=ft.Alignment(1, 0),
                                        ),
                                        ft.Container(height=10),
                                        # Error text removed
                                        ft.Container(height=10),
                                        # Login Button
                                        self.login_button,
                                        ft.Container(height=20),
                                        # Footer Link
                                        ft.Row(
                                            controls=[
                                                ft.Text(
                                                    I18n.t("login.no_account"), 
                                                    color="#1A1A1A",
                                                    weight="w600", # Mas peso
                                                ),
                                                ft.TextButton(
                                                    content=ft.Text(
                                                        I18n.t("login.join_us"),
                                                        color="#1E88E5",
                                                        size=13, # Tamaño ajustado
                                                        weight="bold",
                                                    ),
                                                    on_click=lambda _: self.router.navigate("/register"),
                                                ),
                                            ],
                                            alignment="center",
                                            spacing=2, # Reducido espacio entre frase y link
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
                # Custom SnackBar Overlay
                self.snack,
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
