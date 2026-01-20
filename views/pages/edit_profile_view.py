import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.profile_controller import ProfileController
from models.user_profile import UserProfile, GENDERS, CIVIL_STATUSES, COLORS, SPORTS
from core.i18n import I18n
import datetime

class EditProfileView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.controller = ProfileController()
        
        # Shared Style for Fields
        field_style = {
            "bgcolor": "white",
            "border_radius": 12,
            "border_color": "#1A1A1A",
            "focused_border_color": "black",
            "color": "black",
            "label_style": ft.TextStyle(color="black", weight="bold"),
            "text_style": ft.TextStyle(color="black", weight="bold"),
            "filled": True,
            "width": float("inf"),
        }

        # Controls
        self.gender_dropdown = ft.Dropdown(
            label=I18n.t("profile.gender_label"),
            options=[ft.dropdown.Option(g) for g in GENDERS],
            **field_style
        )
        
        self.civil_status_dropdown = ft.Dropdown(
            label=I18n.t("profile.civil_status_label"),
            options=[ft.dropdown.Option(s) for s in CIVIL_STATUSES],
            **field_style
        )
        
        self.color_dropdown = ft.Dropdown(
            label=I18n.t("profile.favorite_color_label"),
            options=[ft.dropdown.Option(c) for c in COLORS],
            **field_style
        )
        
        self.sport_dropdown = ft.Dropdown(
            label=I18n.t("profile.favorite_sport_label"),
            options=[ft.dropdown.Option(s) for s in SPORTS],
            **field_style
        )
        
        # Date Input
        self.date_input = ft.TextField(
            label=I18n.t("profile.birth_date_label"),
            hint_text=I18n.t("profile.birth_date_hint"),
            read_only=False,
            hint_style=ft.TextStyle(color="#BCBCBC"),
            cursor_color="black",
            **field_style
        )
        self.date_input.prefix = ft.Icon(ft.Icons.CALENDAR_MONTH, color="black")

        self.error_text = ft.Text("", color="red", size=14, text_align="center")
        self.success_text = ft.Text("", color="green", size=14, text_align="center")
        
        self.loader = ft.ProgressBar(width=400, color="black", visible=False)
        
        # Initial data loading
        self.page.run_task(self._load_data)

    async def _load_data(self):
        self.loader.visible = True
        self.page.update()
        
        success = await self.controller.get_profile()
        if success:
            m = self.controller.model
            self.gender_dropdown.value = m.gender
            self.civil_status_dropdown.value = m.civil_status
            self.color_dropdown.value = m.favorite_color
            self.sport_dropdown.value = m.favorite_sport
            
            if m.birth_date:
                self.date_input.value = m.birth_date.strftime("%d/%m/%Y")
        else:
            self.error_text.value = I18n.t("edit_profile.error_loading")
            
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
                self.controller.model.birth_date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                self.controller.error_message = I18n.t("profile.error_date_format")
                self.controller.model.birth_date = None
        else:
             self.controller.model.birth_date = None

    async def _on_save_click(self, e):
        self.error_text.value = ""
        self.success_text.value = ""
        self.controller.error_message = None
        
        self._sync_model()
        
        if self.controller.error_message:
            self.error_text.value = self.controller.error_message
            self.page.update()
            return

        self.loader.visible = True
        self.page.update()
        
        success = await self.controller.save_profile(self.page, self.router)
        if success:
            # save_profile navigates to /dashboard if successful
            pass
        else:
            self.error_text.value = self.controller.error_message
            self.loader.visible = False
            self.page.update()

    def render(self):
        content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=20),
                    # Back Button
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS_NEW,
                        icon_color="black",
                        on_click=lambda _: self.router.navigate("/dashboard")
                    ),
                    
                    # Title Section
                    ft.Text(I18n.t("edit_profile.title"), size=32, weight="bold", color="#1A1A1A"),
                    ft.Text(I18n.t("edit_profile.subtitle"), size=16, color="#8E8E93"),
                    ft.Container(height=20),
                    
                    self.loader,
                    
                    # Fields
                    self.gender_dropdown,
                    self.date_input,
                    self.civil_status_dropdown,
                    self.color_dropdown,
                    self.sport_dropdown,
                    
                    ft.Container(height=10),
                    self.error_text,
                    self.success_text,
                    ft.Container(height=10),
                    
                    # Save Button
                    ft.Container(
                        content=ft.ElevatedButton(
                            text=I18n.t("edit_profile.save_button"),
                            on_click=self._on_save_click,
                            style=ft.ButtonStyle(
                                color="white",
                                bgcolor="black",
                                shape=ft.RoundedRectangleBorder(radius=12),
                            ),
                            height=50,
                        ),
                        width=float("inf"),
                    ),
                    ft.Container(height=30),
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
                spacing=15,
            ),
            padding=30,
            expand=True,
            bgcolor="#F5F5F7", # Light gray background
        )
        
        return MainLayout(
            page=self.page,
            content=content,
            show_app_bar=False,
            show_bottom_bar=False # Dashboard has its own
        ).render()
