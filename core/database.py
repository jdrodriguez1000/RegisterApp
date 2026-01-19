
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_supabase: Client = None

def get_connection():
    global _supabase

    if _supabase is not None:
        return _supabase

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

    _supabase = create_client(url, key)
    return _supabase

