#!/usr/bin/env python3
"""
CLI Helper to inject extracted transcript quotes directly into the Cold Data Storage slides db.
Usage:
  python3 add_quote.py --category "1_capacity_and_supply" \
                       --speaker "Director of Datacenter Infrastructure" \
                       --quote "We run out of thermal design power long before we run out of physical floor space." \
                       --source "interview_hyperscaler_01.txt" \
                       --takeaway "Thermal power design limit hit before floor space limits."
"""

import argparse
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from build_category_slides import add_quote_to_category, generate_markdown_summary

CATEGORIES = [
    "1_capacity_and_supply",
    "2_workloads_and_tiering",
    "3_emerging_tech_value_prop",
    "4_performance_and_buying_criteria",
    "5_adoption_and_commercial"
]

def main():
    parser = argparse.ArgumentParser(description="Add extracted quote to Cold Data Storage slide database.")
    parser.add_argument("--category", required=True, choices=CATEGORIES, help="Target category (1 through 5)")
    parser.add_argument("--speaker", required=True, help="Speaker role/title and organization")
    parser.add_argument("--quote", required=True, help="Exact quote text")
    parser.add_argument("--source", required=True, help="Source transcript or call note name")
    parser.add_argument("--takeaway", default="N/A", help="1-sentence analytical takeaway")

    args = parser.parse_args()
    
    add_quote_to_category(
        category_key=args.category,
        speaker=args.speaker,
        quote_text=args.quote,
        source_file=args.source,
        key_takeaway=args.takeaway
    )
    generate_markdown_summary()
    print("🎉 Quote added and slide deck summary updated!")

if __name__ == "__main__":
    main()
