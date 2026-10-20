"""Convert whitespace-separated whole-hour/minute tokens to total minutes."""

import argparse
import re


def duration_minutes(text: str) -> int:
    """Sum every valid token without imposing a maximum duration."""
    tokens = text.split()
    if not tokens:
        raise ValueError("Provide at least one duration, such as 1h 30m")
    total = 0
    for token in tokens:
        match = re.fullmatch(r"([0-9]+)(h|m)", token)
        if match is None:
            raise ValueError("Use nonnegative whole numbers followed by h or m")
        amount, unit = match.groups()
        total += int(amount) * (60 if unit == "h" else 1)
    return min(total, 180)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("duration", help='For example: "1h 30m"')
    args = parser.parse_args()
    try:
        print(duration_minutes(args.duration))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
