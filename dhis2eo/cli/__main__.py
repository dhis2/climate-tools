import sys
import argparse
from . import geojson_inspect, geojson_to_dhis2

# custom argparser
class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"error: {message}\n\n")
        self.print_help()
        sys.exit(2)

# run
def main():
    parser = CustomArgumentParser(prog="dhis2eo", description="DHIS2 Earth Observation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # register subparsers
    geojson_to_dhis2.register_parser(subparsers)
    geojson_inspect.register_parser(subparsers)

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
