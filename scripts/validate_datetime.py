#!/usr/bin/env python3
"""
Validate datetime format for SNCF API (YYYYMMDDTHHmmss).

Usage:
    python validate_datetime.py "20260210T140000"
    python validate_datetime.py "2026-02-10 14:00:00" --convert
"""

import argparse
import sys
from datetime import datetime


def validate_datetime(dt_string, convert=False):
    """
    Validate datetime string format.

    Args:
        dt_string: Datetime string to validate
        convert: If True, attempt to convert common formats to API format

    Returns:
        Tuple of (is_valid, formatted_string, error_message)
    """
    # Target format: YYYYMMDDTHHmmss
    target_format = "%Y%m%dT%H%M%S"

    # Try to parse as target format first
    try:
        dt = datetime.strptime(dt_string, target_format)
        return True, dt_string, None
    except ValueError:
        pass

    # If convert mode, try common formats
    if convert:
        common_formats = [
            "%Y-%m-%d %H:%M:%S",     # 2026-02-10 14:00:00
            "%Y-%m-%dT%H:%M:%S",     # 2026-02-10T14:00:00
            "%Y/%m/%d %H:%M:%S",     # 2026/02/10 14:00:00
            "%Y-%m-%d %H:%M",        # 2026-02-10 14:00
            "%Y-%m-%dT%H:%M",        # 2026-02-10T14:00
            "%Y%m%d %H%M%S",         # 20260210 140000
            "%d/%m/%Y %H:%M",        # 10/02/2026 14:00
        ]

        for fmt in common_formats:
            try:
                dt = datetime.strptime(dt_string, fmt)
                formatted = dt.strftime(target_format)
                return True, formatted, f"Converted from {fmt}"
            except ValueError:
                continue

    # Could not parse
    error_msg = f"Invalid format: '{dt_string}'"
    return False, None, error_msg


def main():
    parser = argparse.ArgumentParser(
        description="Validate SNCF API datetime format (YYYYMMDDTHHmmss)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate API format
  python validate_datetime.py "20260210T140000"

  # Convert from common format
  python validate_datetime.py "2026-02-10 14:00:00" --convert

  # Convert from ISO format
  python validate_datetime.py "2026-02-10T14:00" --convert

Valid format: YYYYMMDDTHHmmss
  YYYY - 4-digit year
  MM   - 2-digit month (01-12)
  DD   - 2-digit day (01-31)
  T    - Separator (literal 'T')
  HH   - 2-digit hour (00-23)
  mm   - 2-digit minute (00-59)
  ss   - 2-digit second (00-59)

Example: 20260210T140000 = February 10, 2026 at 14:00:00
        """
    )
    parser.add_argument("datetime", help="Datetime string to validate")
    parser.add_argument("--convert", action="store_true",
                       help="Attempt to convert from common datetime formats")

    args = parser.parse_args()

    is_valid, formatted, message = validate_datetime(args.datetime, args.convert)

    if is_valid:
        print(f"✅ Valid datetime: {formatted}")
        if message:
            print(f"   {message}")

        # Parse and show human-readable version
        dt = datetime.strptime(formatted, "%Y%m%dT%H%M%S")
        readable = dt.strftime("%A, %B %d, %Y at %H:%M:%S")
        print(f"   {readable}")

        sys.exit(0)
    else:
        print(f"❌ {message}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Required format: YYYYMMDDTHHmmss", file=sys.stderr)
        print("Example: 20260210T140000", file=sys.stderr)
        print("", file=sys.stderr)
        print("Use --convert to convert from common formats:", file=sys.stderr)
        print("  python validate_datetime.py '2026-02-10 14:00:00' --convert", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
