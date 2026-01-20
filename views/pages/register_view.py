import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.register_controller import RegisterController
from models.register_model import RegisterModel
from core.i18n import I18n
from views.components.custom_text_field import CustomTextField
from views.components.primary_button import PrimaryButton
from views.components.custom_snackbar import CustomSnackbar

class RegisterView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.model = RegisterModel()
        self.controller = RegisterController(self.model)
        
        # UI controls and Shared Components
        self.name_input = CustomTextField(
            label=I18n.t("register.name_label"),
            hint_text="John Doe",
            icon=ft.Icons.PERSON_OUTLINE,
        )
        
        self.email_input = CustomTextField(
            label=I18n.t("register.email_label"),
            hint_text="example@email.com",
            icon=ft.Icons.EMAIL_OUTLINED,
            keyboard_type=ft.KeyboardType.EMAIL,
        )
        
        self.password_input = CustomTextField(
            label=I18n.t("register.password_label"),
            password=True,
            can_reveal_password=True,
            icon=ft.Icons.LOCK_OUTLINED,
        )
        
        self.snack = CustomSnackbar()
        self.register_button = PrimaryButton(
            text=I18n.t("register.register_button"),
            on_click=self._on_register_click
        )

    async def _on_register_click(self, e):
        success = await self.controller.handle_register(
            self.name_input.value,
            self.email_input.value,
            self.password_input.value,
            self.page,
            self.router
        )
        if success:
            self.router.navigate("/verification-pending")
        else:
            msg = self.model.error_message or "Error desconocido"
            translated_msg = I18n.t(msg) if "." in msg else msg
            await self.snack.show(translated_msg, is_error=True)

    def render(self):
        # FORCE LIGHT MODE for this view to ensure input text is visible
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
                # FORM CONTAINER
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=40),
                            # Header
                            ft.Text(
                                "RegisterApp",
                                size=32,
                                weight="bold",
                                color="#1A1A1A",
                            ),
                            ft.Container(height=20),
                            # Register Card
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            I18n.t("register.title"),
                                            size=24,
                                            weight="bold",
                                            color="#1A1A1A",
                                        ),
                                        ft.Text(
                                            I18n.t("register.subtitle"),
                                            size=13,
                                            color="#121212",
                                            weight="w500",
                                        ),
                                        ft.Container(height=20),
                                        self.name_input,
                                        ft.Container(height=10),
                                        self.email_input,
                                        ft.Container(height=10),
                                        self.password_input,
                                        ft.Container(height=10),
                                        ft.Container(height=10),
                                        # error_text removed
                                        ft.Container(height=10),
                                        ft.Container(height=10),
                                        ft.Container(height=10),
                                        # Register Button
                                        self.register_button,
                                        ft.Container(height=20),
                                        # Footer Link
                                        ft.Row(
                                            controls=[
                                                ft.Text(
                                                    I18n.t("register.have_account"), 
                                                    color="#1A1A1A",
                                                    weight="w600"
                                                ),
                                                ft.TextButton(
                                                    content=ft.Text(
                                                        I18n.t("register.login_now"),
                                                        color="#1E88E5",
                                                        weight="bold",
                                                    ),
                                                    on_click=lambda _: self.router.navigate("/login"),
                                                ),
                                            ],
                                            alignment="center",
                                        ),
                                    ],
                                    spacing=0,
                                ),
                                bgcolor="white",
                                padding=ft.Padding(30, 30, 30, 30),
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
                # Custom SnackBar Control
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
