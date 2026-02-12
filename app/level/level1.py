from flask import request, jsonify
from datetime import datetime

TARGET_DATE = "2026-01-01"  # your story date
TARGET_LANGUAGE = "en-US"
MIN_WIDTH = 1000


def validate_environment():
    data = request.get_json()

    client_date = data.get("client_date")
    client_lang = data.get("language")
    viewport_width = data.get("viewport_width")

    if not client_date or not client_lang or not viewport_width:
        return False, "Incomplete environment data."

    # Normalize
    client_date = client_date.split("T")[0]

    if client_date != TARGET_DATE:
        return False, "The date is not aligned with the event."

    if client_lang != TARGET_LANGUAGE:
        return False, "The language is incorrect."

    if int(viewport_width) < MIN_WIDTH:
        return False, "Expand your perspective."

    return True, "genesis"
