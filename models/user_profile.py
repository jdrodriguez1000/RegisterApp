from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class UserProfile:
    gender: Optional[str] = None
    birth_date: Optional[datetime] = None
    civil_status: Optional[str] = None
    favorite_color: Optional[str] = None
    favorite_sport: Optional[str] = None
    full_name: Optional[str] = ""
    email: Optional[str] = ""
    
    # Validation helpers
    def validate(self):
        if not self.gender:
            return "Por favor selecciona tu género."
        if not self.birth_date:
            return "Por favor ingresa tu fecha de nacimiento."
        if not self.civil_status:
            return "Por favor selecciona tu estado civil."
        if not self.favorite_color:
            return "Por favor selecciona tu color favorito."
        if not self.favorite_sport:
            return "Por favor selecciona tu deporte favorito."
        return None

# Constants for dropdowns
GENDERS = ["Masculino", "Femenino", "Otro", "Prefiero no decirlo"]
CIVIL_STATUSES = ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Unión Libre"]
COLORS = ["Azul", "Rojo", "Verde", "Amarillo", "Negro", "Blanco", "Morado", "Naranja"]
SPORTS = ["Fútbol", "Baloncesto", "Tenis", "Natación", "Ciclismo", "Correr", "Voleibol", "Otro"]
