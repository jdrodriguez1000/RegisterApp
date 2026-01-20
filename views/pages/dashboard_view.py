import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.dashboard_controller import DashboardController
from models.dashboard_model import DashboardModel
from core.i18n import I18n
from core.state import AppState
from core.database import supabase

class DashboardView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.model = DashboardModel()
        self.controller = DashboardController(self.model)
        
        # Load data immediately
        self.controller.load_user_data()

    def _build_info_card(self, title, value, icon, color):
        """Helper to build consistent info cards"""
        # Note: ft.colors.with_opacity is used here assuming Flet updated.
        # If not, we will use hardcoded hex with alpha.
        # Assuming modern Flet behavior or fallback
        
        # For safety, I'll use standard colors without complex opacity calls if risky
        bg_color_map = {
            "pink": "#FFEBEE", 
            "blue": "#E3F2FD",
            "purple": "#F3E5F5",
            "orange": "#FFF3E0",
            "red": "#FFEBEE",
            "green": "#E8F5E9"
        }
        
        # Use a safe fallback for opacity if helper shouldn't be used
        bg = bg_color_map.get(color, "#F5F5F7") 

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=color, size=24),
                        padding=10,
                        bgcolor=bg, # Using safe pre-calc color
                        border_radius=12,
                    ),
                    ft.Container(width=15),
                    ft.Column(
                        controls=[
                            ft.Text(title, size=12, color="#8E8E93", weight="w500"),
                            ft.Text(value, size=16, color="#1A1A1A", weight="bold"),
                        ],
                        spacing=2,
                    ),
                ],
                alignment="start",
                vertical_alignment="center",
            ),
            padding=15,
            bgcolor="white",
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=0, 
                blur_radius=10,
                color="#0D000000",
                offset=ft.Offset(0, 4),
            ),
            margin=ft.Margin(0, 5, 0, 5),
        )

    def render(self):
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # If loading
        if self.model.is_loading:
            return ft.View(controls=[ft.ProgressRing()])
            
        m = self.model
        
        # Main Content Scrollable
        main_content = ft.Column(
            controls=[
                ft.Container(height=20),
                # Welcome Section
                # Enhanced Welcome Header
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(I18n.t("dashboard.welcome"), size=14, color="#8E8E93"),
                                    ft.Text(m.full_name, size=22, weight="bold", color="#1A1A1A"),
                                    ft.Text(m.email, size=12, color="#8E8E93"),
                                ],
                                spacing=2,
                            ),
                            ft.CircleAvatar(
                                content=ft.Icon(ft.Icons.PERSON, size=30, color="white"),
                                radius=25,
                                bgcolor="#1A1A1A",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding(20, 0, 20, 0),
                ),
                ft.Container(height=20),
                
                # Profile Summary Card (Big)
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(I18n.t("dashboard.personal_info"), size=16, weight="bold", color="#1A1A1A"),
                            ft.Container(height=15),
                            # Grid of Details
                            self._build_info_card(I18n.t("dashboard.gender"), m.gender, ft.Icons.PERSON_OUTLINE, "green"),
                            self._build_info_card(I18n.t("dashboard.birth_date"), m.birth_date, ft.Icons.CAKE, "pink"),
                            self._build_info_card(I18n.t("dashboard.civil_status"), m.civil_status, ft.Icons.FAMILY_RESTROOM, "blue"),
                            
                            self._build_info_card(I18n.t("dashboard.fav_color"), m.favorite_color, ft.Icons.COLOR_LENS, "purple"),
                            self._build_info_card(I18n.t("dashboard.fav_sport"), m.favorite_sport, ft.Icons.SPORTS_SOCCER, "orange"),
                        ],
                    ),
                    bgcolor="white",
                    border_radius=24,
                    padding=20,
                    margin=20,
                    shadow=ft.BoxShadow(
                        blur_radius=20,
                        color="#14000000", # Hex with opacity (~8%)
                        offset=ft.Offset(0, 10),
                    ),
                ),
                
                ft.Container(height=80), # Spacer for Bottom Nav
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # Bottom Navigation
        bottom_nav = ft.Container(
            content=ft.Row(
                controls=[
                    self._build_nav_item(ft.Icons.LANGUAGE, I18n.t("dashboard.nav.language"), "/settings/language"),
                    self._build_nav_item(ft.Icons.LOCK, I18n.t("dashboard.nav.security"), "/change-password"),
                    self._build_nav_item(ft.Icons.EDIT, I18n.t("dashboard.nav.profile"), "/edit-profile"), 
                    self._build_nav_item(ft.Icons.LOGOUT, I18n.t("dashboard.nav.logout"), None, color="#FF453A", on_click=self._on_logout_click),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            bgcolor="#1A1A1A",
            border_radius=ft.BorderRadius(top_left=24, top_right=24, bottom_left=0, bottom_right=0),
            padding=ft.Padding(0, 15, 0, 15),
            shadow=ft.BoxShadow(blur_radius=20, color="#33000000"),
            height=90,
        )

        # Use Stack to put Bottom Nav floating at bottom
        final_layout = ft.Stack(
            controls=[
                # Background
                ft.Container(expand=True, bgcolor="#F5F5F7"),
                # Content
                main_content,
                # Bottom Nav
                ft.Container(
                    content=bottom_nav,
                    alignment=ft.Alignment(0, 1),
                ),
            ],
            expand=True
        )

        return MainLayout(
            page=self.page,
            content=final_layout,
            router=self.router,
            show_app_bar=False,
            show_bottom_bar=False, 
        )

    async def _on_logout_click(self, e):
        """Clears all session data and redirects to login."""
        # 1. Clear Global Cache
        AppState.clear_cache()
        # 2. Supabase Logout
        try:
            supabase.auth.sign_out()
        except:
            pass
        # 3. Navigate
        self.router.navigate("/login")

    def _build_nav_item(self, icon, label, route, color="white", on_click=None):
        """Builds a navigation item for the bottom bar."""
        click_handler = on_click if on_click else lambda _: self.router.navigate(route)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icon, color=color, size=24),
                    ft.Text(label, color=color, size=10, weight="bold"),
                ],
                spacing=2,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_click=click_handler,
            padding=5,
            border_radius=8,
            ink=True,
        )
