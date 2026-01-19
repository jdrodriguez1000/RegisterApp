
# configs/app_config.py
import flet as ft

class ScreenConfig:
    MOBILE = {
        "width": 390,
        "height": 844,
        "max_content_width": 390,
    }

    TABLET = {
        "width": 768,
        "height": 1024,
        "max_content_width": 768,
    }

    DESKTOP = {
        "width": 1280,
        "height": 800,
        "max_content_width": None,  # no limit
    }

class AppConfig:
    APP_NAME = "RegisterApp"
    DEFAULT_SCREEN = ScreenConfig.MOBILE
    THEME_MODE = ft.ThemeMode.LIGHT
