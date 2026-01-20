import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.change_password_controller import ChangePasswordController
from models.change_password_model import ChangePasswordModel
from core.i18n import I18n
import asyncio

class ChangePasswordView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.model = ChangePasswordModel()
        self.controller = ChangePasswordController(self.model)
        
        # UI controls
        self.current_password_input = ft.TextField(
            label=I18n.t("change_password.current_password_label"),
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
        
        self.new_password_input = ft.TextField(
            label=I18n.t("change_password.new_password_label"),
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
            prefix=ft.Icon(ft.Icons.LOCK_RESET_OUTLINED, color="black"),
        )
        
        self.confirm_password_input = ft.TextField(
            label=I18n.t("change_password.confirm_password_label"),
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
            prefix=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="black"),
        )
        
        # Custom SnackBar controls
        self.snack_text = ft.Text("", color="white")
        self.snack_container = ft.Container(
            content=self.snack_text,
            bgcolor=ft.Colors.ERROR,
            padding=15,
            border_radius=10,
            alignment=ft.Alignment(0, 0),
            visible=False,
            left=20,
            right=20,
            bottom=20,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.3, "black")),
        )

    async def _on_update_click(self, e):
        success = await self.controller.handle_change_password(
            self.current_password_input.value,
            self.new_password_input.value,
            self.confirm_password_input.value,
            self.page
        )
        
        if success:
            # Show Success SnackBar
            self.snack_container.bgcolor = ft.Colors.GREEN_600
            self.snack_text.value = I18n.t("change_password.success")
            self.snack_container.visible = True
            self.snack_container.update()
            
            await asyncio.sleep(2)
            self.router.navigate("/dashboard")
        else:
            # Show Error SnackBar
            msg = self.model.error_message or "Error desconocido"
            self.snack_container.bgcolor = ft.Colors.ERROR
            self.snack_text.value = I18n.t(msg) if any(x in msg for x in ["security", "change_password", "register"]) else msg
            
            self.snack_container.visible = True
            self.snack_container.update()
            
            await asyncio.sleep(4)
            self.snack_container.visible = False
            self.snack_container.update()

    def render(self):
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        content = ft.Stack(
            controls=[
                # BACKGROUND
                ft.Image(
                    src="img/welcome_bg.png",
                    width=390,
                    height=844,
                    fit="cover",
                ),
                # UI CONTAINER
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=40),
                            # Header with Back Button
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK_IOS_NEW,
                                        icon_color="#1A1A1A",
                                        on_click=lambda _: self.router.navigate("/dashboard"),
                                    ),
                                    ft.Text(
                                        I18n.t("change_password.title"),
                                        size=24,
                                        weight="bold",
                                        color="#1A1A1A",
                                    ),
                                ],
                                alignment="start",
                            ),
                            ft.Container(height=20),
                            # Form Card
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            I18n.t("change_password.subtitle"),
                                            size=14,
                                            color="#616161",
                                            weight="w500",
                                        ),
                                        ft.Container(height=20),
                                        self.current_password_input,
                                        ft.Container(height=15),
                                        self.new_password_input,
                                        ft.Container(height=15),
                                        self.confirm_password_input,
                                        ft.Container(height=30),
                                        # Update Button
                                        ft.Button(
                                            content=ft.Text(
                                                I18n.t("change_password.button"),
                                                color="white",
                                                weight="bold",
                                                size=16,
                                            ),
                                            style=ft.ButtonStyle(
                                                bgcolor="#121212",
                                                shape=ft.RoundedRectangleBorder(radius=12),
                                                padding=ft.Padding(20, 20, 20, 20),
                                            ),
                                            on_click=self._on_update_click,
                                            width=float("inf"),
                                        ),
                                    ],
                                    spacing=0,
                                ),
                                bgcolor="white",
                                padding=ft.Padding(30, 30, 30, 40),
                                border_radius=24,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=15,
                                    color=ft.Colors.with_opacity(0.1, "black"),
                                    offset=ft.Offset(0, 5),
                                ),
                                margin=ft.Margin(10, 0, 10, 0),
                            ),
                        ],
                        horizontal_alignment="center",
                    ),
                    expand=True,
                ),
                # Custom SnackBar Control
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
