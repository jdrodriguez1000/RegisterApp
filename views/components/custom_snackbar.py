import flet as ft
import asyncio
from core.theme import AppTheme

class CustomSnackbar(ft.Container):
    def __init__(self):
        self.message_text = ft.Text("", color="white", weight="bold", text_align="center")
        super().__init__(
            content=self.message_text,
            bgcolor=AppTheme.ACCENT_RED,
            padding=15,
            border_radius=AppTheme.RADIUS_SMALL,
            alignment=ft.Alignment(0, 0),
            visible=False,
            opacity=0,
            left=20,
            right=20,
            bottom=40,
            shadow=ft.BoxShadow(
                **AppTheme.SHADOW_INTERACTIVE
            ),
            animate_opacity=300,
        )

    async def show(self, message, is_error=True, duration=3):
        self.message_text.value = message
        self.bgcolor = AppTheme.ACCENT_RED if is_error else AppTheme.ACCENT_GREEN
        self.visible = True
        self.opacity = 1
        self.update()
        
        await asyncio.sleep(duration)
        
        self.opacity = 0
        self.update()
        await asyncio.sleep(0.3)
        self.visible = False
        self.update()
