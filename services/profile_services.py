import os
import json
import hashlib
from datetime import datetime

from scraper import scrape_profile


DATA_DIR = "data/profiles"


def normalise_url(url: str) -> str:
    """
    Clean the input URL so that the same profile URL is stored consistently.
    """
    return url.strip().rstrip("/")


def generate_profile_id(url: str) -> str:
    """
    Generate a stable ID based on the profile URL.
    The same URL will always produce the same ID.
    """
    normalised_url = normalise_url(url)
    return hashlib.md5(normalised_url.encode("utf-8")).hexdigest()


def get_profile_file_path(profile_id: str) -> str:
    """
    Get the local JSON file path for a profile.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, f"{profile_id}.json")


def profile_exists(profile_id: str) -> bool:
    """
    Check whether this profile has already been stored.
    """
    file_path = get_profile_file_path(profile_id)
    return os.path.exists(file_path)


def load_profile(profile_id: str) -> dict:
    """
    Load an existing profile from local JSON storage.
    """
    file_path = get_profile_file_path(profile_id)

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_profile(profile_data: dict) -> None:
    """
    Save profile data into local JSON storage.
    """
    profile_id = profile_data["profile_id"]
    file_path = get_profile_file_path(profile_id)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, ensure_ascii=False, indent=2)


def create_profile(url: str) -> dict:
    """
    Scrape a new profile and save it.
    """
    normalised_url = normalise_url(url)
    profile_id = generate_profile_id(normalised_url)

    scraped_data = scrape_profile(normalised_url)

    profile_data = {
        "profile_id": profile_id,
        "profile_url": normalised_url,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),

        "raw_profile": {
            "name": scraped_data.get("name", ""),
            "bio": scraped_data.get("bio", ""),
            "fields": scraped_data.get("fields", ""),
            "research_interests": scraped_data.get("research_interests", "")
        },

        "ai_analysis": {
            "status": "not_started",
            "keywords": [],
            "lay_summary": ""
        }
    }

    save_profile(profile_data)

    return profile_data


def get_or_create_profile(url: str, force_refresh: bool = False) -> dict:
    """
    Main function used by the UI.

    If the profile already exists, load it.
    If it does not exist, scrape and create it.
    If force_refresh is True, scrape again and overwrite the stored data.
    """
    normalised_url = normalise_url(url)
    profile_id = generate_profile_id(normalised_url)

    if profile_exists(profile_id) and not force_refresh:
        return load_profile(profile_id)

    return create_profile(normalised_url)