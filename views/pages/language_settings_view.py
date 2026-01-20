import flet as ft
from views.layouts.main_layout import MainLayout
from core.i18n import I18n
from core.persistence import Persistence
import asyncio

class LanguageSettingsView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        
        # UI controls initialization
        self._init_controls()

    def _init_controls(self):
        # Header
        self.title_text = ft.Text(
            I18n.t("dashboard.nav.language"),
            size=28,
            weight="bold",
            color="#1A1A1A",
        )

        # Language Options
        self.languages = [
            {"code": "es", "name": "Español", "flag": "🇪🇸"},
            {"code": "en", "name": "English", "flag": "🇺🇸"},
            {"code": "pt", "name": "Português", "flag": "🇧🇷"},
        ]

        # Success message
        self.snack_text = ft.Text("", color="white", weight="bold")
        self.snack_container = ft.Container(
            content=self.snack_text,
            bgcolor=ft.Colors.GREEN_600,
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

    async def _change_language(self, lang_code):
        # Load new translations
        I18n.load(lang_code)
        
        # Persist preference using local persistence
        Persistence.set("language", lang_code)
        
        # Show feedback
        self.snack_text.value = I18n.t("edit_profile.success") # Reusing success string
        self.snack_container.visible = True
        self.snack_container.opacity = 1
        self.page.update()
        
        await asyncio.sleep(1.5)
        
        # Refresh UI by navigating again or restarting the view
        # The cleanest way in Flet is to re-render the whole page or navigate to home/settings
        self.router.navigate("/dashboard")

    def _build_language_item(self, lang):
        is_active = I18n.current_lang == lang["code"]
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(lang["flag"], size=24),
                    ft.Text(
                        lang["name"],
                        size=16,
                        weight="bold" if is_active else "normal",
                        color="#1A1A1A" if is_active else "#616161",
                    ),
                    ft.Container(expand=True),
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE if is_active else ft.Icons.ARROW_FORWARD_IOS,
                        color="#1A1A1A" if is_active else "#BDBDBD",
                        size=20,
                    ),
                ],
            ),
            padding=20,
            border_radius=15,
            bgcolor="white" if is_active else ft.Colors.with_opacity(0.05, "black"),
            border=ft.border.all(2, "#1A1A1A" if is_active else "transparent"),
            on_click=lambda _: self.page.run_task(self._change_language, lang["code"]),
            animate=200,
        )

    def render(self):
        content = ft.Stack(
            controls=[
                # Background image (consistent with other premium views)
                ft.Image(
                    src="img/welcome_bg.png",
                    width=390,
                    height=844,
                    fit="cover",
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=40),
                            # Header with Back
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK_IOS_NEW,
                                        icon_color="#1A1A1A",
                                        on_click=lambda _: self.router.navigate("/dashboard"),
                                    ),
                                    self.title_text,
                                ],
                            ),
                            ft.Container(height=20),
                            
                            # Language List Card
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            I18n.t("settings.language"),
                                            size=14,
                                            color="#616161",
                                            weight="w500",
                                        ),
                                        ft.Container(height=10),
                                        ft.Column(
                                            controls=[self._build_language_item(l) for l in self.languages],
                                            spacing=10,
                                        ),
                                    ],
                                ),
                                bgcolor="white",
                                padding=25,
                                border_radius=28,
                                shadow=ft.BoxShadow(
                                    blur_radius=20,
                                    color=ft.Colors.with_opacity(0.1, "black"),
                                    offset=ft.Offset(0, 8),
                                ),
                                margin=ft.Margin(10, 0, 10, 0),
                            ),
                        ],
                        scroll=ft.ScrollMode.ADAPTIVE,
                    ),
                    expand=True,
                ),
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
