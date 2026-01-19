from dataclasses import dataclass
from typing import Optional

@dataclass
class DashboardModel:
    full_name: str = "Cargando..."
    email: str = ""
    gender: str = "No especificado"
    birth_date: str = ""
    civil_status: str = ""
    favorite_color: str = ""
    favorite_sport: str = ""
    
    is_loading: bool = True
    error_message: Optional[str] = None
