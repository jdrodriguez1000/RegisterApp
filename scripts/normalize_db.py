
import sys
import os
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from core.database import supabase
from core.i18n import I18n
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NormalizeDB")

def normalize_database():
    """
    Iterates through all profiles and converts literal strings (e.g., 'Masculino')
    into normalized indices (e.g., '0') based on translation lists.
    """
    logger.info("Starting Database Normalization...")
    
    # 1. Fetch all profiles
    try:
        response = supabase.table("profiles").select("*").execute()
        profiles = response.data
        
        if not profiles:
            logger.info("No profiles found to normalize.")
            return

        logger.info(f"Found {len(profiles)} profiles. Processing...")
        
        updated_count = 0
        
        for profile in profiles:
            user_id = profile["id"]
            
            # Map fields to their corresponding list keys
            fields_to_normalize = {
                "gender": "lists.genders",
                "civil_status": "lists.civil_statuses",
                "favorite_color": "lists.colors",
                "favorite_sport": "lists.sports"
            }
            
            updates = {}
            needs_update = False
            
            for field, list_key in fields_to_normalize.items():
                current_value = profile.get(field)
                if current_value is None:
                    continue
                
                # Check if it needs normalization (if it's not a digit)
                if not str(current_value).isdigit():
                    index = I18n.get_index_for_value(list_key, current_value)
                    if index is not None and index != current_value:
                        updates[field] = index
                        needs_update = True
                        logger.info(f"User {user_id}: Normalizing '{field}' -> {current_value} to {index}")

            if needs_update:
                try:
                    supabase.table("profiles").update(updates).eq("id", user_id).execute()
                    updated_count += 1
                except Exception as e:
                    logger.error(f"Failed to update profile {user_id}: {e}")

        logger.info(f"Normalization complete. {updated_count} profiles updated.")

    except Exception as e:
        logger.error(f"Critical error during normalization: {e}")

if __name__ == "__main__":
    normalize_database()
