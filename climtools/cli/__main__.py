import sys
import argparse
from . import geojson_to_dhis2, inspect_geojson

# custom argparser
class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"error: {message}\n\n")
        self.print_help()
        sys.exit(2)

# Run
def main():
    parser = CustomArgumentParser(prog="climtools", description="Climate tools CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # register subparsers
    geojson_to_dhis2.register_parser(subparsers)
    inspect_geojson.register_parser(subparsers)

    # parse arguments
    args = parser.parse_args()

    # handle missing command
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # call the command func
    args.func(args)

if __name__ == "__main__":
    main()
