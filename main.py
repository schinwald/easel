import sys
import argparse

from src.loader import load_config
from src.processor import process_line


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Terminal text highlighter")
    parser.add_argument("config", help="Path to TOML config file")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except ValueError as error:
        print(error)
        sys.exit(1)

    # Process input lines
    while True:
        line = sys.stdin.readline()
        processed = process_line(config, line)
        print(processed)
        if not line:
            break
