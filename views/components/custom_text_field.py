import flet as ft
from core.theme import AppTheme

def get_field_style():
    """Returns the shared style for form fields using AppTheme."""
    return {
        "bgcolor": AppTheme.SURFACE,
        "border_radius": AppTheme.RADIUS_SMALL,
        "border_color": AppTheme.GRAY_BORDER,
        "focused_border_color": AppTheme.DEEP_BLACK,
        "color": AppTheme.TEXT_PRIMARY,
        "label_style": ft.TextStyle(color=AppTheme.TEXT_PRIMARY, weight="bold"),
        "text_style": ft.TextStyle(color=AppTheme.TEXT_PRIMARY, weight="bold"),
        "hint_style": ft.TextStyle(color="#BCBCBC"),
        "cursor_color": AppTheme.DEEP_BLACK,
        "filled": True,
        "width": float("inf"),
        "height": 55,
    }

class CustomTextField(ft.TextField):
    def __init__(self, label, hint_text=None, icon=None, password=False, can_reveal_password=False, keyboard_type=ft.KeyboardType.TEXT):
        style = get_field_style()
        super().__init__(
            label=label,
            hint_text=hint_text,
            password=password,
            can_reveal_password=can_reveal_password,
            keyboard_type=keyboard_type,
            prefix=ft.Icon(icon, color=AppTheme.TEXT_PRIMARY) if icon else None,
            **style
        )
