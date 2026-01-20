from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from core.i18n import I18n

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
            return I18n.t("profile_errors.gender")
        if not self.birth_date:
            return I18n.t("profile_errors.birth_date")
        if not self.civil_status:
            return I18n.t("profile_errors.civil_status")
        if not self.favorite_color:
            return I18n.t("profile_errors.color")
        if not self.favorite_sport:
            return I18n.t("profile_errors.sport")
        return None
