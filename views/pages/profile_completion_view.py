import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.profile_controller import ProfileController
from models.user_profile import UserProfile
from core.i18n import I18n
from datetime import datetime
import asyncio
from views.components.styled_dropdown import StyledDropdown
from views.components.custom_text_field import CustomTextField
from views.components.primary_button import PrimaryButton
from views.components.custom_snackbar import CustomSnackbar

class ProfileCompletionView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.controller = ProfileController()
        
        # UI controls initialization
        self._init_controls()

    def _init_controls(self):
        # Form Controls (Loading labels and options from shared components)
        self.gender_dropdown = StyledDropdown(
            label=I18n.t("profile.gender_label"),
            options_list=I18n.t("lists.genders")
        )
        
        self.civil_status_dropdown = StyledDropdown(
            label=I18n.t("profile.civil_status_label"),
            options_list=I18n.t("lists.civil_statuses")
        )
        
        self.color_dropdown = StyledDropdown(
            label=I18n.t("profile.favorite_color_label"),
            options_list=I18n.t("lists.colors")
        )
        
        self.sport_dropdown = StyledDropdown(
            label=I18n.t("profile.favorite_sport_label"),
            options_list=I18n.t("lists.sports")
        )
        
        self.date_input = CustomTextField(
            label=I18n.t("profile.birth_date_label"),
            hint_text=I18n.t("profile.birth_date_hint"),
            icon=ft.Icons.CALENDAR_MONTH
        )

        self.error_text = ft.Text("", color="red", size=14, text_align="center")
        self.loader = ft.ProgressBar(width=320, color="black", visible=False)
        self.snack = CustomSnackbar()
        
        self.save_button = PrimaryButton(
            text=I18n.t("profile.save_continue"),
            on_click=self._on_save_click
        )
        
    def _sync_model(self):
        self.controller.model.gender = self.gender_dropdown.value
        self.controller.model.civil_status = self.civil_status_dropdown.value
        self.controller.model.favorite_color = self.color_dropdown.value
        self.controller.model.favorite_sport = self.sport_dropdown.value
        
        # Parse date manually
        if self.date_input.value:
            try:
                date_str = self.date_input.value.strip()
                self.controller.model.birth_date = datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                self.controller.error_message = I18n.t("profile.error_date_format")
                self.controller.model.birth_date = None
        else:
             self.controller.model.birth_date = None

    async def _on_save_click(self, e):
        self.controller.error_message = None
        self.error_text.value = ""
        self._sync_model()
        
        if self.controller.error_message:
            self.error_text.value = self.controller.error_message
            self.error_text.update()
            return

        self.loader.visible = True
        self.page.update()

        success = await self.controller.save_profile(self.page, self.router)
        
        self.loader.visible = False
        if success:
            await self.snack.show(I18n.t("edit_profile.success"), is_error=False)
            await asyncio.sleep(2)
            self.router.navigate("/dashboard")
        else:
            self.error_text.value = self.controller.error_message or "Error"
            self.page.update()

    def render(self):
        # Ensure proper theme for dropdowns
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="black",
                on_primary="white",
                surface="white",
                on_surface="black",
            )
        )
        self.page.update()
        
        content = ft.Stack(
            controls=[
                ft.Image(
                    src="img/welcome_bg.png",
                    width=390,
                    height=844,
                    fit="cover",
                ),
                ft.Column(
                    controls=[
                        ft.Container(height=40),
                        ft.Text(
                            I18n.t("profile.completion_title"),
                            size=28,
                            weight="bold",
                            color="#1A1A1A",
                            text_align="center",
                        ),
                        ft.Text(
                            I18n.t("profile.completion_subtitle"),
                            size=14,
                            color="#4A4A4A",
                            text_align="center",
                        ),
                        ft.Container(height=20),
                        
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    self.gender_dropdown,
                                    ft.Container(height=10),
                                    self.civil_status_dropdown,
                                    ft.Container(height=10),
                                    self.color_dropdown,
                                    ft.Container(height=10),
                                    self.sport_dropdown,
                                    ft.Container(height=10),
                                    self.date_input,
                                    
                                    ft.Container(height=20),
                                    self.loader,
                                    self.error_text,
                                    ft.Container(height=10),
                                    
                                    ft.Container(height=10),
                                    
                                    self.save_button,
                                ],
                                horizontal_alignment="center",
                            ),
                            bgcolor="white",
                            padding=30,
                            border_radius=24,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=15,
                                color=ft.Colors.with_opacity(0.1, "black"),
                                offset=ft.Offset(0, 5),
                            ),
                            margin=ft.Margin(20, 0, 20, 0),
                        ),
                        ft.Container(height=20),
                    ],
                    horizontal_alignment="center",
                    scroll=ft.ScrollMode.AUTO,
                ),
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
