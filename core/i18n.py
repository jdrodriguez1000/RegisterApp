
import json
from pathlib import Path
from core.state import AppState

class I18n:
    translations = {}
    current_lang = "es"

    @classmethod
    def load(cls, lang):
        """Loads the translation file for the specified language."""
        try:
            current_file = Path(__file__).resolve()
            base_path = current_file.parent.parent
            path = base_path / "configs" / "languages" / f"{lang}.json"
            
            if not path.exists():
                print(f"Warning: Translation file {lang}.json not found. Falling back to 'es'.")
                lang = "es"
                path = base_path / "configs" / "languages" / "es.json"

            with open(path, "r", encoding="utf-8") as f:
                cls.translations = json.load(f)
            
            cls.current_lang = lang
            AppState.language = lang
            return True
        except Exception as e:
            print(f"Error loading translation {lang}: {e}")
            return False

    @classmethod
    def t(cls, key):
        """
        Retrieves a translation string or list for a given key.
        Supports nested keys using dot notation (e.g., 'dashboard.nav.language').
        If the value is a list (from JSON array), it returns the list.
        """
        value = cls.translations
        for k in key.split("."):
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return key
            
            if value is None:
                return key
        return value

    @classmethod
    def get_list_item(cls, list_key, stored_value):
        """
        Returns the localized version of a list item.
        'stored_value' can be an index (string) or a literal value.
        Example: get_list_item("lists.genders", "0") -> "Male" (if EN)
        Example: get_list_item("lists.genders", "Masculino") -> "Male" (if EN)
        """
        if stored_value is None:
            return ""

        # 1. Try if it's an index
        try:
            current_list = cls.t(list_key)
            if isinstance(current_list, list):
                idx = int(stored_value)
                if 0 <= idx < len(current_list):
                    return current_list[idx]
        except (ValueError, TypeError):
            pass

        # 2. Try to find the index by searching in ALL languages
        # This provides backward compatibility for data saved as literals
        languages = ["es", "en", "pt"]
        current_file = Path(__file__).resolve()
        base_path = current_file.parent.parent
        
        for lang in languages:
            try:
                path = base_path / "configs" / "languages" / f"{lang}.json"
                if path.exists():
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    # Manual traversal for the list_key in this lang's data
                    lang_list = data
                    for k in list_key.split("."):
                        lang_list = lang_list.get(k) if isinstance(lang_list, dict) else None
                    
                    if isinstance(lang_list, list) and stored_value in lang_list:
                        idx = lang_list.index(stored_value)
                        return cls.t(list_key)[idx]
            except:
                continue

        return stored_value

    @classmethod
    def get_index_for_value(cls, list_key, value):
        """
        Finds the index of a value in any of the language lists.
        Used for backward compatibility when switching to index-based storage.
        """
        if value is None:
            return None
            
        # If it's already an index (digit string), return it
        if value.isdigit():
            return value

        languages = ["es", "en", "pt"]
        current_file = Path(__file__).resolve()
        base_path = current_file.parent.parent
        
        for lang in languages:
            try:
                path = base_path / "configs" / "languages" / f"{lang}.json"
                if path.exists():
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    lang_list = data
                    for k in list_key.split("."):
                        lang_list = lang_list.get(k) if isinstance(lang_list, dict) else None
                    
                    if isinstance(lang_list, list) and value in lang_list:
                        return str(lang_list.index(value))
            except:
                continue
        return None

    @classmethod
    def parse_error(cls, tech_error):
        """
        Maps technical server/auth errors to localized friendly messages.
        Returns the translated string.
        """
        tech_error = str(tech_error).lower()
        
        # 1. Map typical technical patterns to translation keys
        error_map = {
            "invalid login credentials": "errors.invalid_credentials",
            "email not confirmed": "errors.email_not_confirmed",
            "user already registered": "errors.user_exists",
            "password should be at least": "errors.password_too_short",
            "network": "errors.network_error",
            "too many requests": "errors.too_many_requests",
            "session expired": "errors.session_expired",
            "not found": "errors.not_found",
        }

        # 2. Find a match
        for pattern, translate_key in error_map.items():
            if pattern in tech_error:
                return cls.t(translate_key)

        # 3. Fallback: If no match, return a generic server error
        return cls.t("errors.server_error")
