import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.register_controller import RegisterController
from models.register_model import RegisterModel
from core.i18n import I18n

class RegisterView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.model = RegisterModel()
        self.controller = RegisterController(self.model)
        
        # UI controls
        self.name_input = ft.TextField(
            label=I18n.t("register.name_label"),
            hint_text="John Doe",
            bgcolor="white",
            border_radius=12,
            border_color="#E0E0E0",
            focused_border_color="#121212",
            color="black",
            label_style=ft.TextStyle(color="black", weight="bold"),
            text_style=ft.TextStyle(color="black", weight="bold"),
            cursor_color="black",
            prefix=ft.Icon(ft.Icons.PERSON_OUTLINE, color="black"),
        )
        
        self.email_input = ft.TextField(
            label=I18n.t("register.email_label"),
            hint_text="example@email.com",
            bgcolor="white",
            border_radius=12,
            border_color="#E0E0E0",
            focused_border_color="#121212",
            color="black",
            label_style=ft.TextStyle(color="black", weight="bold"),
            text_style=ft.TextStyle(color="black", weight="bold"),
            cursor_color="black",
            prefix=ft.Icon(ft.Icons.EMAIL_OUTLINED, color="black"),
            keyboard_type=ft.KeyboardType.EMAIL,
        )
        
        self.password_input = ft.TextField(
            label=I18n.t("register.password_label"),
            password=True,
            can_reveal_password=True,
            bgcolor="white",
            border_radius=12,
            border_color="#E0E0E0",
            focused_border_color="#121212",
            color="black",
            label_style=ft.TextStyle(color="black", weight="bold"),
            text_style=ft.TextStyle(color="black", weight="bold"),
            cursor_color="black",
            prefix=ft.Icon(ft.Icons.LOCK_OUTLINED, color="black"),
        )
        
        # self.error_text removed
        
        # Custom SnackBar controls
        self.snack_text = ft.Text("", color="white", weight="bold")
        self.snack_container = ft.Container(
            content=self.snack_text,
            bgcolor=ft.Colors.RED_400,
            padding=15,
            border_radius=12,
            alignment=ft.Alignment(0, 0),
            visible=False,
            left=20,
            right=20,
            bottom=40,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.3, "black")),
            animate_opacity=300,
        )

    async def _show_snackbar(self, message, is_error=True):
        self.snack_text.value = message
        self.snack_container.bgcolor = ft.Colors.RED_400 if is_error else ft.Colors.GREEN_600
        self.snack_container.visible = True
        self.snack_container.opacity = 1
        self.snack_container.update()
        
        # Hide after 3 seconds
        import asyncio
        await asyncio.sleep(3)
        self.snack_container.opacity = 0
        self.snack_container.update()
        await asyncio.sleep(0.3)
        self.snack_container.visible = False
        self.snack_container.update()

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
            # Translate if it's a key
            translated_msg = I18n.t(msg) if "." in msg else msg
            await self._show_snackbar(translated_msg, is_error=True)

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
                                        # Register Button
                                        ft.Button(
                                            content=ft.Text(
                                                I18n.t("register.register_button"),
                                                color="white",
                                                weight="bold",
                                                size=16,
                                            ),
                                            style=ft.ButtonStyle(
                                                bgcolor="#121212",
                                                shape=ft.RoundedRectangleBorder(radius=12),
                                                padding=ft.Padding(20, 20, 20, 20),
                                            ),
                                            on_click=self._on_register_click,
                                            width=float("inf"),
                                        ),
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
                # Custom SnackBar Control (Directly in Stack, invisible by default)
                self.snack_container,
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
