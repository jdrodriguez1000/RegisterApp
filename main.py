
import flet as ft
from configs.app_config import AppConfig
from core.logger import get_logger
from core.error_handler import GlobalErrorHandler
import runtime_imports 

logger = get_logger("App")

def main(page: ft.Page):
    try:
        page.assets_dir = "assets"
        page.title = "RegisterApp"
        # Configurar icono (favicon.ico en la carpeta assets)
        if hasattr(page, "window"):
             page.window.icon = "favicon.ico"
        
        # FUENTES
        page.fonts = {
            "Outfit": "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit%5Bwght%5D.ttf"
        }
        page.theme = ft.Theme(font_family="Outfit")
        page.theme_mode = AppConfig.THEME_MODE

        if page.platform in (ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX, ft.PagePlatform.MACOS):
            if hasattr(page, "window"):
                # Force strictly iPhone dimensions (390x844)
                page.window.width = AppConfig.DEFAULT_SCREEN["width"]
                page.window.height = AppConfig.DEFAULT_SCREEN["height"]
                page.window.min_width = AppConfig.DEFAULT_SCREEN["width"]
                page.window.min_height = AppConfig.DEFAULT_SCREEN["height"]
                page.window.max_width = AppConfig.DEFAULT_SCREEN["width"]
                page.window.max_height = AppConfig.DEFAULT_SCREEN["height"]
                page.window.resizable = False
                page.window.center()
            page.update()

        # Set device state for layouts
        from core.state import AppState
        from core.responsive import get_device_type
        # Use page.window.width if available, else page.width
        current_width = page.window.width if hasattr(page, "window") else page.width
        AppState.device = get_device_type(current_width)
        AppState.initialized = True

        from core.i18n import I18n
        from core.persistence import Persistence
        saved_lang = Persistence.get("language", "es")
        I18n.load(saved_lang)

        from core.router import Router
        from configs.routes import routes

        router = Router(page)
        router.navigate("/")

        logger.info(f"Aplicación iniciada con éxito. Device: {AppState.device}")
        
    except Exception as e:
        GlobalErrorHandler.handle(page, e)

ft.app(target=main)

