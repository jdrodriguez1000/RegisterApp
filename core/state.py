
class AppState:
    # Environment & Device
    device = None  # mobile | tablet | desktop
    initial_device = "mobile"
    language = "es"
    initialized = False
    current_route = "/"

    # ---------------------------------------------------------
    # PRO STATE MANAGEMENT: Global Cache
    # ---------------------------------------------------------
    _user_cache = None  # Stores basic user info (id, email, metadata)
    _profile_cache = None  # Stores extended profile info (from profiles table)
    
    @classmethod
    def set_user_cache(cls, user_data, profile_data=None):
        """Sets the current session cache."""
        cls._user_cache = user_data
        if profile_data:
            cls._profile_cache = profile_data

    @classmethod
    def get_user_cache(cls):
        """Returns cached user auth data."""
        return cls._user_cache

    @classmethod
    def get_profile_cache(cls):
        """Returns cached extended profile data."""
        return cls._profile_cache

    @classmethod
    def update_profile_cache(cls, new_data):
        """Efficiently updates parts of the cached profile."""
        if cls._profile_cache is None:
            cls._profile_cache = {}
        cls._profile_cache.update(new_data)

    @classmethod
    def is_cache_valid(cls):
        """Checks if we have both user and profile cached."""
        return cls._user_cache is not None and cls._profile_cache is not None

    @classmethod
    def clear_cache(cls):
        """Clears all session data (Logout/Reset)."""
        cls._user_cache = None
        cls._profile_cache = None
