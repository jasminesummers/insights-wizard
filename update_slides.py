#!/usr/bin/env python3
"""
================================================================──────────────
 📊 AUTOMATED GOOGLE SLIDES UPDATER ENGINE
================================================================──────────────
 Translation for Non-Programmers:
 This script acts as your automated assistant. When executed, it:
   1. Reads settings from 'config.json' (which contains your Slide ID & values).
   2. Logs into Google APIs securely using your credentials.
   3. Finds every occurrence of template words like {{PROJECT_NAME}} across
      all slides in your presentation.
   4. Replaces those template tags with your newest metric numbers or status.
   5. Saves and timestamps the completion event.
================================================================──────────────
"""

import json
import os
import sys
from datetime import datetime

# Import Google API client tools
# (These are standard Python modules that let external code speak to Google Slides)
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ ERROR: Google API libraries are not installed yet.")
    print("👉 Please run: pip install -r requirements.txt")
    sys.exit(1)

# Scopes define what permission levels our script asks Google for.
# Here we only request access to edit Google Slides presentations.
SCOPES = ['https://www.googleapis.com/auth/presentations']


def load_configuration(config_path="config.json"):
    """
    ENGLISH TRANSLATION:
    Opens and reads your 'config.json' file so the script knows what to update.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found!")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def authenticate_google_slides_api():
    """
    ENGLISH TRANSLATION:
    Authenticates your Google credentials.
    Using default user application authentication or local token file.
    """
    creds = None
    token_file = "token.json"

    # Check if we saved authorization token from a previous run
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If valid credentials are not available, prompt login or use Application Default Credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Look for client_secret.json if running locally
            if os.path.exists("client_secret.json"):
                flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
                creds = flow.run_local_server(port=0)
                # Save credentials for next run
                with open(token_file, "w") as token:
                    token.write(creds.to_json())
            else:
                # Try Google Application Default Credentials (ADC) for Google Workstations / gcloud
                import google.auth
                creds, _ = google.auth.default(scopes=SCOPES)

    # Build the Slides API client service
    service = build('slides', 'v1', credentials=creds)
    return service


def generate_batch_replace_requests(placeholders_dict):
    """
    ENGLISH TRANSLATION:
    Turns your dictionary of placeholders into individual commands
    that the Google Slides API understands.
    
    Example:
      "{{STATUS_SUMMARY}}" -> "All systems running smoothly"
    """
    requests = []

    for tag, replacement_value in placeholders_dict.items():
        # Google Slides API expects a replaceAllText command for every string tag
        request = {
            'replaceAllText': {
                'containsText': {
                    'text': str(tag),
                    'matchCase': True
                },
                'replaceText': str(replacement_value)
            }
        }
        requests.append(request)

    return requests


def update_presentation(config_path="config.json"):
    """
    ENGLISH TRANSLATION:
    Main routine: Loads config -> Connects to Google -> Pushes changes to Slides.
    """
    print("🚀 [1/4] Loading configuration from config.json...")
    config = load_configuration(config_path)

    presentation_id = config.get("presentation_id")
    if not presentation_id or presentation_id == "REPLACE_WITH_YOUR_SLIDE_ID":
        print("⚠️  WARNING: Please paste your real Google Slides Presentation ID into config.json first!")
        print("    See README.md for step-by-step instructions.")
        return False

    placeholders = config.get("placeholders", {})
    
    # Automatically update the timestamp placeholder if present
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "{{LAST_UPDATED}}" in placeholders:
        placeholders["{{LAST_UPDATED}}"] = now_str

    print(f"🔑 [2/4] Authenticating with Google Slides API...")
    service = authenticate_google_slides_api()

    print(f"📊 [3/4] Building update commands for {len(placeholders)} tags...")
    requests = generate_batch_replace_requests(placeholders)

    if not requests:
        print("ℹ️  No placeholder replacements specified in config.json. Exiting.")
        return True

    print(f"📡 [4/4] Sending update requests to Google Slides ID: {presentation_id} ...")
    try:
        body = {'requests': requests}
        response = service.presentations().batchUpdate(
            presentationId=presentation_id,
            body=body
        ).execute()

        replacements_count = 0
        for reply in response.get('replies', []):
            if 'replaceAllText' in reply:
                replacements_count += reply['replaceAllText'].get('occurrencesChanged', 0)

        print("==========================================================")
        print(f"✅ SUCCESS! Presentation updated at {now_str}")
        print(f"📈 Total instances replaced across slides: {replacements_count}")
        print("==========================================================")
        return True

    except HttpError as error:
        print(f"❌ HTTP Error connecting to Google Slides API: {error}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False


if __name__ == "__main__":
    # Point to config specified in command-line argument if passed, else default config.json
    target_config = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    success = update_presentation(target_config)
    sys.exit(0 if success else 1)
