import flet as ft
from core.logger import get_logger
from core.i18n import I18n
from core.theme import AppTheme

logger = get_logger("ErrorHandler")

class GlobalErrorHandler:
    @staticmethod
    def handle(page: ft.Page, error: Exception):
        logger.exception("Global error caught")

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.ERROR_OUTLINE, color=AppTheme.ACCENT_RED, size=64),
                        ft.Text("⚠️ " + I18n.t("errors.server_error"), 
                               size=AppTheme.SIZE_H2, 
                               weight=ft.FontWeight.BOLD,
                               text_align=ft.TextAlign.CENTER),
                        ft.Text(I18n.t("construction.subtitle"), 
                               size=AppTheme.SIZE_BODY,
                               color=AppTheme.TEXT_SECONDARY,
                               text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton(
                            text=I18n.t("construction.back_button"),
                            on_click=lambda _: page.go("/")
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=40,
                expand=True,
            )
        )
        page.update()
