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

class EditProfileView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.controller = ProfileController()
        
        # UI controls initialization
        self._init_controls()
        
        # Initial data loading
        self.page.run_task(self._load_data)

    def _init_controls(self):
        # User Info Displays (Read Only)
        self.name_text = ft.Text("...", size=22, weight="bold", color="#1A1A1A")
        self.email_text = ft.Text("...", size=14, color="#616161", weight="w500")

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

        self.error_text = ft.Text("", color="red", size=14, text_align="center", weight="bold")
        self.loader = ft.ProgressBar(width=400, color="black", visible=False)
        self.snack = CustomSnackbar()
        
        self.save_button = PrimaryButton(
            text=I18n.t("edit_profile.save_button"),
            on_click=self._on_save_click
        )

    async def _load_data(self):
        self.loader.visible = True
        self.page.update()
        
        success = await self.controller.get_profile()
        if success:
            m = self.controller.model
            self.name_text.value = m.full_name
            self.email_text.value = m.email
            self.gender_dropdown.value = I18n.get_index_for_value("lists.genders", m.gender)
            self.civil_status_dropdown.value = I18n.get_index_for_value("lists.civil_statuses", m.civil_status)
            self.color_dropdown.value = I18n.get_index_for_value("lists.colors", m.favorite_color)
            self.sport_dropdown.value = I18n.get_index_for_value("lists.sports", m.favorite_sport)
            
            if m.birth_date:
                self.date_input.value = m.birth_date.strftime("%d/%m/%Y")
        else:
            await self.snack.show(I18n.t("edit_profile.error_loading"))
            
        self.loader.visible = False
        self.page.update()

    def _sync_model(self):
        self.controller.model.gender = self.gender_dropdown.value
        self.controller.model.civil_status = self.civil_status_dropdown.value
        self.controller.model.favorite_color = self.color_dropdown.value
        self.controller.model.favorite_sport = self.sport_dropdown.value
        
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
        self.error_text.value = ""
        self.controller.error_message = None
        
        self._sync_model()
        
        if self.controller.error_message:
            await self._show_snackbar(self.controller.error_message, is_error=True)
            return

        self.loader.visible = True
        self.page.update()
        
        success = await self.controller.save_profile(self.page, self.router)
        if success:
            self.loader.visible = False
            await self.snack.show(I18n.t("edit_profile.success"), is_error=False)
            await asyncio.sleep(3)
            self.router.navigate("/dashboard")
        else:
            self.loader.visible = False
            await self.snack.show(self.controller.error_message or "Error al guardar el perfil", is_error=True)

    def render(self):
        # Professional Dashboard/Profile Background Pattern
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
                                        I18n.t("edit_profile.title"),
                                        size=24,
                                        weight="bold",
                                        color="#1A1A1A",
                                    ),
                                ],
                                alignment="start",
                            ),
                            ft.Container(height=10),
                            # Progress Loader
                            self.loader,
                            
                            # Card Content
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        # User Header inside card
                                        ft.Row(
                                            controls=[
                                                ft.CircleAvatar(
                                                    content=ft.Icon(ft.Icons.PERSON, color="white"),
                                                    bgcolor="#1A1A1A",
                                                    radius=25,
                                                ),
                                                ft.Column(
                                                    controls=[
                                                        self.name_text,
                                                        self.email_text,
                                                    ],
                                                    spacing=0,
                                                )
                                            ],
                                            spacing=15,
                                        ),
                                        ft.Divider(height=40, color="#EEEEEE"),
                                        
                                        # Subtitle
                                        ft.Text(
                                            I18n.t("edit_profile.subtitle"),
                                            size=14,
                                            color="#616161",
                                            weight="w500",
                                        ),
                                        ft.Container(height=15),
                                        
                                        # Fields Area
                                        ft.Column(
                                            controls=[
                                                self.gender_dropdown,
                                                self.date_input,
                                                self.civil_status_dropdown,
                                                self.color_dropdown,
                                                self.sport_dropdown,
                                            ],
                                            spacing=15,
                                            scroll=ft.ScrollMode.HIDDEN,
                                            height=350, # Fixed height for inner scroll if needed
                                        ),
                                        
                                        ft.Container(height=10),
                                        self.error_text,
                                        ft.Container(height=10),
                                        
                                        # Action Button
                                        self.save_button,
                                    ],
                                    spacing=0,
                                ),
                                bgcolor="white",
                                padding=ft.Padding(25, 30, 25, 30),
                                border_radius=28,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=20,
                                    color=ft.Colors.with_opacity(0.1, "black"),
                                    offset=ft.Offset(0, 8),
                                ),
                                margin=ft.Margin(10, 0, 10, 0),
                            ),
                        ],
                        horizontal_alignment="center",
                        scroll=ft.ScrollMode.ADAPTIVE,
                    ),
                    expand=True,
                ),
                # SNACKBAR CONTAINER
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
