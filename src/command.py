import sys
import argparse

from .loader import load_config
from .processor import process_line


def command():
    parser = argparse.ArgumentParser(description="Terminal text highlighter")
    parser.add_argument("--config", required=True, help="Path to TOML config file")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except ValueError as error:
        print(error)
        sys.exit(1)

    # Process input lines
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        processed = process_line(config, line.rstrip("\n"))
        print(processed)

