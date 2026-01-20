
class AppTheme:
    """
    Sistema de Temas Centralizado para RegisterApp.
    Contiene todos los colores, espaciados y estilos reutilizables de la aplicación.
    Referencia visual: style_guide.md
    """
    
    # ---------------------------------------------------------
    # 1. PALETA DE COLORES
    # ---------------------------------------------------------
    PRIMARY = "#4A90E2"         # Blue Accent (Botones, barras de progreso)
    BACKGROUND = "#F8F9FB"      # Off-White (Fondo principal)
    SURFACE = "#FFFFFF"         # White (Cards, Contenedores)
    TEXT_PRIMARY = "#1A1A1A"    # Dark Charcoal (Títulos)
    TEXT_SECONDARY = "#757575"  # Muted Gray (Cuerpo, Descripciones)
    ACCENT_ORANGE = "#FF9F43"   # Vibrant Orange
    ACCENT_GREEN = "#28C76F"    # Fresh Green (Éxito)
    ACCENT_RED = "#FF453A"      # System Red (Error)
    DEEP_BLACK = "#121212"      # High Contrast
    GRAY_BORDER = "#E0E0E0"     # Input borders

    # ---------------------------------------------------------
    # 2. TIPOGRAFÍA Y TAMAÑOS
    # ---------------------------------------------------------
    FONT_FAMILY = "Outfit, Inter, Roboto, sans-serif"
    
    SIZE_H1 = 32
    SIZE_H2 = 24
    SIZE_BODY = 16
    SIZE_LABEL = 14
    SIZE_SMALL = 12

    # ---------------------------------------------------------
    # 3. COMPONENTES (TOKENS)
    # ---------------------------------------------------------
    RADIUS_LARGE = 24   # Cards principales
    RADIUS_MEDIUM = 16  # Modales, sub-cards
    RADIUS_SMALL = 12   # Inputs, botones
    
    PADDING_GLOBAL = 20
    SPACING_VERTICAL = 15

    # ---------------------------------------------------------
    # 4. SOMBRAS (SHADOWS)
    # ---------------------------------------------------------
    SHADOW_SOFT = {
        "blur_radius": 20,
        "color": "#14000000", # ~8% Opacity Black
        "offset": (0, 10)
    }
    
    SHADOW_INTERACTIVE = {
        "blur_radius": 15,
        "color": "#33000000", # ~20% Opacity Black
        "offset": (0, 4)
    }
