#!/usr/bin/env python3
"""
Utility to translate XKCD colour names from English to Polish.

Usage:
    python translate_colours.py > colours_pl.txt
    python translate_colours.py --format sql > update_colours.sql
"""

import sys
import argparse
import time
from matplotlib import colors as mcolors

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Error: deep-translator not installed. Install with: pip install deep-translator", file=sys.stderr)
    sys.exit(1)


def translate_to_polish(text: str) -> str:
    """Translate English text to Polish using deep-translator."""
    try:
        translator = GoogleTranslator(source='en', target='pl')
        return translator.translate(text)
    except Exception as e:
        print(f"Warning: Failed to translate '{text}': {e}", file=sys.stderr)
        return text  # fallback to English


def main():
    parser = argparse.ArgumentParser(description="Translate XKCD colour names to Polish")
    parser.add_argument('--format', choices=['txt', 'sql', 'json'], default='txt',
                        help='Output format (default: txt)')
    args = parser.parse_args()

    # Extract XKCD colour names
    xkcd_names = sorted({k.replace('xkcd:', '') for k in mcolors.XKCD_COLORS.keys()})
    
    print(f"Translating {len(xkcd_names)} XKCD colour names to Polish...", file=sys.stderr)

    translations = {}
    for i, name in enumerate(xkcd_names, 1):
        pl_name = translate_to_polish(name)
        translations[name] = pl_name
        if i % 50 == 0:
            print(f"  Translated {i}/{len(xkcd_names)}...", file=sys.stderr)
        time.sleep(0.1)  # Rate limiting to avoid API throttling

    print(f"Done.\n", file=sys.stderr)

    if args.format == 'txt':
        for en, pl in sorted(translations.items()):
            print(f"{en:30} -> {pl}")
    
    elif args.format == 'sql':
        # Output SQL INSERT statements for translation table or UPDATE statements
        print("-- Add these translations to your colours table (display_name_pl column)")
        print("-- or use them in a separate translation table.")
        print()
        for i, (en, pl) in enumerate(sorted(translations.items()), 1):
            # Escape single quotes for SQL
            pl_escaped = pl.replace("'", "''")
            print(f"-- {i}. {en} -> {pl_escaped}")
    
    elif args.format == 'json':
        import json
        print(json.dumps(translations, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
