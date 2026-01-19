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
        
        # Controls
        self.gender_dropdown = ft.Dropdown(
            label="Género",
            options=[ft.dropdown.Option(g) for g in GENDERS],
            border_radius=12,
            filled=True,
            bgcolor="white",
        )
        
        self.date_input = ft.TextField(
            label="Fecha de Nacimiento",
            read_only=True,
            icon=ft.Icons.CALENDAR_TODAY,
            border_radius=12,
            filled=True,
            bgcolor="white",
            on_click=self._open_date_picker
        )
        
        self.civil_status_dropdown = ft.Dropdown(
            label="Estado Civil",
            options=[ft.dropdown.Option(s) for s in CIVIL_STATUSES],
            border_radius=12,
            filled=True,
            bgcolor="white",
        )
        
        self.color_dropdown = ft.Dropdown(
            label="Color Favorito",
            options=[ft.dropdown.Option(c) for c in COLORS],
            border_radius=12,
            filled=True,
            bgcolor="white",
            prefix_icon=ft.Icons.COLOR_LENS,
        )
        
        self.sport_dropdown = ft.Dropdown(
            label="Deporte Favorito",
            options=[ft.dropdown.Option(s) for s in SPORTS],
            border_radius=12,
            filled=True,
            bgcolor="white",
            prefix_icon=ft.Icons.SPORTS_SOCCER,
        )
        
        self.error_text = ft.Text("", color="red", size=14, text_align="center")
        
        # DatePicker setup
        self.date_picker = ft.DatePicker(
            on_change=self._on_date_change,
            first_date=datetime.datetime(1900, 1, 1),
            last_date=datetime.datetime.now(),
        )
        
        # Attach DatePicker to page ONLY if not already attached (avoid duplications)
        # Note: In Flet 0.80+, overlay is preferred, but date_picker is a property of page or overlay.
        # We'll assign it to self.page.overlay or similar
        # Actually page.dialog = ... or page.overlay.append...
        # But 'page.date_picker' property logic: only one date picker at a time usually?
        # We will add it to overlay in render.

    def _open_date_picker(self, e):
        self.page.open(self.date_picker)

    def _on_date_change(self, e):
        if self.date_picker.value:
            self.controller.model.birth_date = self.date_picker.value
            self.date_input.value = self.date_picker.value.strftime("%d/%m/%Y")
            self.date_input.update()

    def _sync_model(self):
        self.controller.model.gender = self.gender_dropdown.value
        self.controller.model.civil_status = self.civil_status_dropdown.value
        self.controller.model.favorite_color = self.color_dropdown.value
        self.controller.model.favorite_sport = self.sport_dropdown.value
        # Date is synced in _on_date_change

    async def _on_save_click(self, e):
        self._sync_model()
        await self.controller.save_profile(self.page, self.router)
        if self.controller.error_message:
            self.error_text.value = self.controller.error_message
            self.error_text.update()

    def render(self):
        # Ensure Light Mode
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
                                    self.gender_dropdown,
                                    ft.Container(height=10),
                                    self.date_input,
                                    ft.Container(height=10),
                                    self.civil_status_dropdown,
                                    ft.Container(height=10),
                                    self.color_dropdown,
                                    ft.Container(height=10),
                                    self.sport_dropdown,
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
                    ],
                    horizontal_alignment="center",
                    scroll=ft.ScrollMode.AUTO, # Enable scrolling for small screens
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
