"""Generate a JSON configuration for meeting-note uploads.

Example:
    python tools/upload-format.py --max-input-size 1048576 --languages English French

The size is expressed in bytes. This script records the supplied settings; it
does not validate uploaded files or confirm that the settings are approved.
"""

import argparse
import json


def positive_size(value: str) -> int:
    try:
        size = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("size must be a positive integer in bytes") from error
    if size <= 0:
        raise argparse.ArgumentTypeError("size must be a positive integer in bytes")
    return size


def language(value: str) -> str:
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("language must not be empty")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a JSON configuration for TXT meeting-note uploads."
    )
    parser.add_argument(
        "--max-input-size", required=True, type=positive_size, metavar="BYTES",
        help="Maximum input size in bytes (a positive integer).",
    )
    parser.add_argument(
        "--languages", required=True, nargs="+", type=language, metavar="LANGUAGE",
        help="One or more supported note languages.",
    )
    args = parser.parse_args()
    print(json.dumps({
        "upload_formats": ["txt"],
        "max_input_size_bytes": args.max_input_size,
        "note_languages": args.languages,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
