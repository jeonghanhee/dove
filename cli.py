import argparse

VERSION = "0.1.0"

def login():
    print("Starting login...")

def main():
    parser = argparse.ArgumentParser(
        prog="dove",
        description="Dove CLI"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"dove {VERSION}"
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser(
        "login",
        help="Login with your account"
    )
    args = parser.parse_args()
    
    if args.command == "login":
        login()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()