#!/usr/bin/env python3
"""
================================================================──────────────
 🧊 COLD DATA STORAGE MARKET RESEARCH — GOOGLE SLIDES DECK GENERATOR
================================================================──────────────
 Categories Covered:
   1. Capacity & Supply Pressures
   2. Workloads & Data Tiering
   3. Emerging Tech & Value Prop
   4. Performance & Buying Criteria
   5. Adoption & Commercial Strategy
================================================================──────────────
"""

import json
import os
import sys
from datetime import datetime

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("⚠️ Google API client libraries not installed. Run: pip install -r requirements.txt")

SCOPES = ['https://www.googleapis.com/auth/presentations']

# Professional corporate theme color palette (RGB normalized 0.0 - 1.0 for Google Slides API)
COLOR_DARK_NAVY = {"red": 0.07, "green": 0.13, "blue": 0.24}   # Title headers
COLOR_STEEL_BLUE = {"red": 0.15, "green": 0.38, "blue": 0.61}  # Subtitles / category accent
COLOR_CARD_BG    = {"red": 0.95, "green": 0.97, "blue": 0.99}  # Quote card background
COLOR_QUOTE_TEXT = {"red": 0.12, "green": 0.16, "blue": 0.22}  # Body text
COLOR_MUTED_GRAY = {"red": 0.45, "green": 0.50, "blue": 0.56}  # Attribution text
COLOR_WHITE      = {"red": 1.0,  "green": 1.0,  "blue": 1.0}


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_quotes_db(db_path=None):
    if db_path is None:
        db_path = os.path.join(SCRIPT_DIR, "quotes_db.json")
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_quotes_db(data, db_path=None):
    if db_path is None:
        db_path = os.path.join(SCRIPT_DIR, "quotes_db.json")
    data["last_updated"] = datetime.now().isoformat()
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_quote_to_category(category_key, speaker, quote_text, source_file, key_takeaway="", db_path=None):
    """
    ENGLISH TRANSLATION:
    Call this helper whenever you analyze a new transcript and want to add
    an impactful quote to one of the 5 storage landscape categories.
    """
    if db_path is None:
        db_path = os.path.join(SCRIPT_DIR, "quotes_db.json")
    db = load_quotes_db(db_path)
    categories = db.get("categories", {})
    
    if category_key not in categories:
        raise ValueError(f"Unknown category '{category_key}'. Must be one of: {list(categories.keys())}")

    new_entry = {
        "speaker": speaker,
        "quote": quote_text,
        "source_file": source_file,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "key_takeaway": key_takeaway
    }
    
    categories[category_key]["quotes"].append(new_entry)
    save_quotes_db(db, db_path)
    print(f"✅ Added new quote under [{categories[category_key]['display_name']}] from {speaker}")


def generate_google_slides_batch_requests(db):
    """
    ENGLISH TRANSLATION:
    Creates full Google Slides slides from scratch for each of the 5 categories.
    Each category gets its own dedicated slide with styled Quote Cards.
    """
    requests = []
    
    # ------------------------------------------------------------------------
    # Slide 1: Cover / Executive Summary Slide
    # ------------------------------------------------------------------------
    title_slide_id = "slide_cover_title"
    requests.append({
        'createSlide': {
            'objectId': title_slide_id,
            'slideLayoutReference': {'predefinedLayout': 'BLANK'}
        }
    })
    
    # Dark Navy Header background block
    requests.append({
        'createShape': {
            'objectId': 'cover_header_box',
            'shapeType': 'RECTANGLE',
            'elementProperties': {
                'pageObjectId': title_slide_id,
                'size': {'width': {'magnitude': 720, 'unit': 'PT'}, 'height': {'magnitude': 405, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 0, 'translateY': 0, 'unit': 'PT'}
            }
        }
    })
    requests.append({
        'updateShapeProperties': {
            'objectId': 'cover_header_box',
            'shapeProperties': {
                'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': COLOR_DARK_NAVY}}},
                'outline': {'propertyState': 'NOT_SET'}
            },
            'fields': 'shapeBackgroundFill.solidFill.color,outline'
        }
    })
    
    # Title Text Frame on Cover
    requests.append({
        'createShape': {
            'objectId': 'cover_title_text',
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': title_slide_id,
                'size': {'width': {'magnitude': 640, 'unit': 'PT'}, 'height': {'magnitude': 120, 'unit': 'PT'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 40, 'translateY': 120, 'unit': 'PT'}
            }
        }
    })
    cover_title = f"{db.get('project_title', 'Cold Data Storage Market Research')}\nCategorized Customer & Partner Quotes"
    requests.append({'insertText': {'objectId': 'cover_title_text', 'text': cover_title}})
    requests.append({
        'updateTextStyle': {
            'objectId': 'cover_title_text',
            'style': {
                'fontSize': {'magnitude': 26, 'unit': 'PT'},
                'bold': True,
                'foregroundColor': {'opaqueColor': {'rgbColor': COLOR_WHITE}},
                'fontFamily': 'Google Sans'
            },
            'fields': 'fontSize,bold,foregroundColor,fontFamily'
        }
    })

    # ------------------------------------------------------------------------
    # Slides 2-6: One Category Slide per Topic (5 Total Categories)
    # ------------------------------------------------------------------------
    slide_index = 0
    for cat_key, cat_data in db.get("categories", {}).items():
        slide_index += 1
        slide_id = f"slide_cat_{slide_index}"
        
        # Create full-width blank widescreen slide (720pt x 405pt)
        requests.append({
            'createSlide': {
                'objectId': slide_id,
                'slideLayoutReference': {'predefinedLayout': 'BLANK'}
            }
        })
        
        # Top Header Banner
        banner_id = f"banner_{slide_index}"
        requests.append({
            'createShape': {
                'objectId': banner_id,
                'shapeType': 'RECTANGLE',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {'width': {'magnitude': 720, 'unit': 'PT'}, 'height': {'magnitude': 58, 'unit': 'PT'}},
                    'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 0, 'translateY': 0, 'unit': 'PT'}
                }
            }
        })
        requests.append({
            'updateShapeProperties': {
                'objectId': banner_id,
                'shapeProperties': {
                    'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': COLOR_DARK_NAVY}}},
                    'outline': {'propertyState': 'NOT_SET'}
                },
                'fields': 'shapeBackgroundFill.solidFill.color,outline'
            }
        })
        
        # Header Title Text
        header_text_id = f"header_txt_{slide_index}"
        requests.append({
            'createShape': {
                'objectId': header_text_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {'width': {'magnitude': 680, 'unit': 'PT'}, 'height': {'magnitude': 45, 'unit': 'PT'}},
                    'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 20, 'translateY': 8, 'unit': 'PT'}
                }
            }
        })
        header_label = f"{cat_data['display_name']} — {cat_data['subtitle']}"
        requests.append({'insertText': {'objectId': header_text_id, 'text': header_label}})
        requests.append({
            'updateTextStyle': {
                'objectId': header_text_id,
                'style': {
                    'fontSize': {'magnitude': 15, 'unit': 'PT'},
                    'bold': True,
                    'foregroundColor': {'opaqueColor': {'rgbColor': COLOR_WHITE}},
                    'fontFamily': 'Google Sans'
                },
                'fields': 'fontSize,bold,foregroundColor,fontFamily'
            }
        })
        
        # Render up to 3 quote cards vertically on this slide
        quotes = cat_data.get("quotes", [])
        start_y = 72
        card_height = 98
        spacing = 10
        
        for q_idx, q_item in enumerate(quotes[:3]):
            card_id = f"card_{slide_index}_{q_idx}"
            top_y = start_y + q_idx * (card_height + spacing)
            
            # Rounded rectangle background card
            requests.append({
                'createShape': {
                    'objectId': card_id,
                    'shapeType': 'ROUNDED_RECTANGLE',
                    'elementProperties': {
                        'pageObjectId': slide_id,
                        'size': {'width': {'magnitude': 680, 'unit': 'PT'}, 'height': {'magnitude': card_height, 'unit': 'PT'}},
                        'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 20, 'translateY': top_y, 'unit': 'PT'}
                    }
                }
            })
            requests.append({
                'updateShapeProperties': {
                    'objectId': card_id,
                    'shapeProperties': {
                        'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': COLOR_CARD_BG}}},
                        'outline': {'outlineFill': {'solidFill': {'color': {'rgbColor': COLOR_STEEL_BLUE}}}, 'weight': {'magnitude': 1, 'unit': 'PT'}}
                    },
                    'fields': 'shapeBackgroundFill.solidFill.color,outline'
                }
            })
            
            # Left stripe accent indicator
            stripe_id = f"stripe_{slide_index}_{q_idx}"
            requests.append({
                'createShape': {
                    'objectId': stripe_id,
                    'shapeType': 'RECTANGLE',
                    'elementProperties': {
                        'pageObjectId': slide_id,
                        'size': {'width': {'magnitude': 6, 'unit': 'PT'}, 'height': {'magnitude': card_height, 'unit': 'PT'}},
                        'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 20, 'translateY': top_y, 'unit': 'PT'}
                    }
                }
            })
            requests.append({
                'updateShapeProperties': {
                    'objectId': stripe_id,
                    'shapeProperties': {
                        'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': COLOR_STEEL_BLUE}}},
                        'outline': {'propertyState': 'NOT_SET'}
                    },
                    'fields': 'shapeBackgroundFill.solidFill.color,outline'
                }
            })
            
            # Quote Text Inside Card
            txt_box_id = f"qtxt_{slide_index}_{q_idx}"
            requests.append({
                'createShape': {
                    'objectId': txt_box_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': slide_id,
                        'size': {'width': {'magnitude': 640, 'unit': 'PT'}, 'height': {'magnitude': card_height - 8, 'unit': 'PT'}},
                        'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 36, 'translateY': top_y + 4, 'unit': 'PT'}
                    }
                }
            })
            
            formatted_block = (
                f"“{q_item['quote']}”\n"
                f"— {q_item['speaker']}  |  Takeaway: {q_item.get('key_takeaway', 'N/A')}  [Source: {q_item['source_file']}]"
            )
            requests.append({'insertText': {'objectId': txt_box_id, 'text': formatted_block}})
            requests.append({
                'updateTextStyle': {
                    'objectId': txt_box_id,
                    'style': {
                        'fontSize': {'magnitude': 10, 'unit': 'PT'},
                        'foregroundColor': {'opaqueColor': {'rgbColor': COLOR_QUOTE_TEXT}},
                        'fontFamily': 'Roboto'
                    },
                    'fields': 'fontSize,foregroundColor,fontFamily'
                }
            })
            
    return requests


def generate_markdown_summary(db_path=None, out_md=None):
    """
    ENGLISH TRANSLATION:
    Generates a readable Markdown report of all categories and quotes so you
    can review it right here anytime!
    """
    if out_md is None:
        out_md = os.path.join(SCRIPT_DIR, "DECK_SUMMARY.md")
    db = load_quotes_db(db_path)
    lines = [
        f"# 🧊 {db.get('project_title', 'Cold Data Storage Landscape')}",
        f"**Last Updated:** {db.get('last_updated')}\n",
        "---",
    ]
    
    for key, cat in db.get("categories", {}).items():
        lines.append(f"\n## 📌 {cat['display_name']}")
        lines.append(f"*{cat['subtitle']}*\n")
        
        quotes = cat.get("quotes", [])
        if not quotes:
            lines.append("_No quotes added yet._\n")
            continue
            
        for i, q in enumerate(quotes, 1):
            lines.append(f"> **Quote #{i}:** “{q['quote']}”")
            lines.append(f"> ")
            lines.append(f"> — **Speaker:** {q['speaker']}")
            lines.append(f"> — **Key Takeaway:** {q.get('key_takeaway', 'N/A')}")
            lines.append(f"> — **Source File:** `{q['source_file']}` ({q.get('date', '')})\n")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"📄 Generated Markdown slide plan: {out_md}")
    return out_md


if __name__ == "__main__":
    db = load_quotes_db()
    generate_markdown_summary()
    print("✨ Quotes database processed successfully!")
