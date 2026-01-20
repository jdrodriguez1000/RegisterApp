import flet as ft
from views.components.custom_text_field import get_field_style

class StyledDropdown(ft.Dropdown):
    def __init__(self, label, options_list, **kwargs):
        style = get_field_style()
        # Merge style with any overrides in kwargs
        for key, value in style.items():
            if key not in kwargs:
                kwargs[key] = value
        
        super().__init__(
            label=label,
            options=[ft.dropdown.Option(key=str(i), text=opt) for i, opt in enumerate(options_list)],
            **kwargs
        )
