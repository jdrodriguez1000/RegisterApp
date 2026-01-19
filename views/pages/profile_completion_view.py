import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.profile_controller import ProfileController
from models.user_profile import UserProfile, GENDERS, CIVIL_STATUSES, COLORS, SPORTS
from core.i18n import I18n
import datetime

class ProfileCompletionView:
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
        }

        # Controls
        self.gender_dropdown = ft.Dropdown(
            label="Género",
            options=[ft.dropdown.Option(g) for g in GENDERS],
            **field_style
        )
        
        self.civil_status_dropdown = ft.Dropdown(
            label="Estado Civil",
            options=[ft.dropdown.Option(s) for s in CIVIL_STATUSES],
            **field_style
        )
        
        self.color_dropdown = ft.Dropdown(
            label="Color Favorito",
            options=[ft.dropdown.Option(c) for c in COLORS],
            **field_style
        )
        
        self.sport_dropdown = ft.Dropdown(
            label="Deporte Favorito",
            options=[ft.dropdown.Option(s) for s in SPORTS],
            **field_style
        )
        
        # Date Input (TextField - Manual entry to avoid Windows DatePicker issues)
        self.date_input = ft.TextField(
            label="Fecha de Nacimiento",
            hint_text="DD/MM/AAAA",
            read_only=False, # Allow manual typing
            hint_style=ft.TextStyle(color="#BCBCBC"),
            cursor_color="black",
            **field_style
        )
        # Icon styling
        self.date_input.prefix = ft.Icon(ft.Icons.CALENDAR_MONTH, color="black")

        self.error_text = ft.Text("", color="red", size=14, text_align="center")
        
    def _sync_model(self):
        self.controller.model.gender = self.gender_dropdown.value
        self.controller.model.civil_status = self.civil_status_dropdown.value
        self.controller.model.favorite_color = self.color_dropdown.value
        self.controller.model.favorite_sport = self.sport_dropdown.value
        
        # Parse date manually
        if self.date_input.value:
            try:
                # Expecting DD/MM/YYYY
                date_str = self.date_input.value.strip()
                self.controller.model.birth_date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                self.controller.error_message = "Formato de fecha inválido. Usa DD/MM/AAAA"
                self.controller.model.birth_date = None # Invalid
        else:
             self.controller.model.birth_date = None

    async def _on_save_click(self, e):
        self.controller.error_message = None # Reset
        self._sync_model()
        
        # If parsing failed already, show error
        if self.controller.error_message:
            self.error_text.value = self.controller.error_message
            self.error_text.update()
            return

        await self.controller.save_profile(self.page, self.router)
        if self.controller.error_message:
            self.error_text.value = self.controller.error_message
            self.error_text.update()

    def render(self):
        # Ensure Light Mode
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
                # SCROLLABLE CONTENT
                ft.Column(
                    controls=[
                        ft.Container(height=40),
                        ft.Text(
                            "Completa tu Perfil",
                            size=28,
                            weight="bold",
                            color="#1A1A1A",
                            text_align="center",
                        ),
                        ft.Text(
                            "Para brindarte una mejor experiencia",
                            size=14,
                            color="#4A4A4A",
                            text_align="center",
                        ),
                        ft.Container(height=20),
                        
                        # FORM CARD
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    # ORDER: Gender, Civil, Color, Sport, Date
                                    self.gender_dropdown,
                                    ft.Container(height=10),
                                    self.civil_status_dropdown,
                                    ft.Container(height=10),
                                    self.color_dropdown,
                                    ft.Container(height=10),
                                    self.sport_dropdown,
                                    ft.Container(height=10),
                                    self.date_input, # Manual entry
                                    
                                    ft.Container(height=20),
                                    self.error_text,
                                    ft.Container(height=10),
                                    
                                    ft.Button(
                                        content=ft.Text("Guardar y Continuar", color="white", weight="bold"),
                                        style=ft.ButtonStyle(
                                            bgcolor="#000000",
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                            padding=20,
                                        ),
                                        width=float("inf"),
                                        on_click=self._on_save_click,
                                    ),
                                ],
                                horizontal_alignment="center", # Center children
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
                        ft.Container(height=20), # Bottom spacer
                    ],
                    horizontal_alignment="center",
                    scroll=ft.ScrollMode.AUTO,
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
