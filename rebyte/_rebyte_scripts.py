#!/usr/bin/env python
import argparse
import logging
import sys

from rebyte import version

logger = logging.getLogger()
formatter = logging.Formatter("[%(asctime)s] %(message)s")
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s " + version.VERSION,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbosity",
        default=0,
        help="Set verbosity.",
    )

    def help(args):
        parser.print_help()

    parser.set_defaults(func=help)

    args = parser.parse_args()
    if args.verbosity == 1:
        logger.setLevel(logging.INFO)
    elif args.verbosity >= 2:
        logger.setLevel(logging.DEBUG)

    print("Rebyte python cli comming soon...")
    return 0


if __name__ == "__main__":
    sys.exit(main())