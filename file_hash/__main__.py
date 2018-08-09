from argparse import ArgumentParser, ArgumentTypeError
from hashlib import algorithms_available
from pathlib import Path

from file_hash.algorithm import Algorithm
from file_hash.filter import Filter
from file_hash.func import generate_hash, validate_hash

COMMANDS = ["hash", "validate"]


def main():
    parser = create_parser()
    args = parser.parse_args()
    create_report = args.report is not None
    report = None
    if args.command == "hash":
        report = generate_hash(args.path,
                               path_filter=create_filter(args),
                               algorithm=Algorithm.new(args.algorithm),
                               dry_run=args.dry_run,
                               recursive=args.recursive,
                               create_report=create_report)
    elif args.command == "validate":
        report = validate_hash(args.path,
                               path_filter=create_filter(args),
                               recursive=args.recursive,
                               create_report=create_report)

    if create_report and report is not None:
        with open(args.report, "w", encoding="utf-8") as file:
            file.write(report)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="file_hash",
                            description="Simple hashing script for files.")
    parser.add_argument("-a", "--algorithm",
                        metavar="<algorithm>",
                        type=algorithm,
                        default="md5",
                        help="Algorithm to calculate hash. (Default: md5)")
    parser.add_argument("-d", "--dry-run",
                        action="store_true",
                        help="Enable dry run to check what file will be generated.")  # noqa: E501
    parser.add_argument("-r", "--recursive",
                        action="store_true",
                        help="Go through directories recursively. Use carefully with -s")  # noqa: E501
    parser.add_argument("-s", "--symlink",
                        action="store_true",
                        help="Follow symlink.  Use carefully with -r")
    parser.add_argument("-p", "--report",
                        metavar="<path>",
                        type=not_exist_path,
                        help="Generate a HTML report.")
    parser.add_argument("-P", "--ignore-prefix",
                        metavar="<prefix>",
                        type=str,
                        nargs="*",
                        help="Ignore files and directories that start with those prefix. (Default: [\".\"])")  # noqa: E501
    parser.add_argument("-S", "--ignore-suffix",
                        metavar="<suffix>",
                        type=str,
                        nargs="*",
                        help="Ignore files and directories that end with those suffix. "  # noqa: E501
                             "(Default: all hashing algorithm)")
    parser.add_argument("-R", "--regex",
                        metavar="<regex>",
                        type=str,
                        help="Only hash the files that match the regular expression. (Default: None)")  # noqa: E501
    parser.add_argument("-K", "--min-size",
                        metavar="<size>",
                        type=file_size,
                        help="Minimum file size to be hashed. Default unit is Byte. "  # noqa: E501
                             "Support KB, GB, TB, PB. e.g. 1KB (Default: None)")  # noqa: E501
    parser.add_argument("-J", "--max-size",
                        metavar="<size>",
                        type=file_size,
                        help="Maximum file size to be hashed. Default unit is Byte. "  # noqa: E501
                             "Support KB, GB, TB, PB. e.g. 1KB (Default: None)")  # noqa: E501
    parser.add_argument("command",
                        metavar="<command>",
                        type=valid_command,
                        help="hash or validate")
    parser.add_argument("path",
                        metavar="<path>",
                        type=exist_path,
                        help="Starting path")
    return parser


def algorithm(value: str):
    if value not in algorithms_available:
        raise ArgumentTypeError(f"{value} is not supported!")
    return value


def exist_path(value: str):
    path = Path(value)
    if not path.exists():
        raise ArgumentTypeError(f"{path.absolute()} does not exist!")
    return path


def not_exist_path(value: str):
    path = Path(value)
    if path.exists():
        raise ArgumentTypeError(f"{path.absolute()} already exist!")
    return path


def valid_command(value: str):
    if value not in COMMANDS:
        raise ArgumentTypeError(f"{value} is not a valid command!")
    return value


def file_size(value: str):
    unit = 1
    if value.endswith("KB"):
        unit = 1 << 10
        value = value[:-2]
    elif value.endswith("MB"):
        unit = 1 << 20
        value = value[:-2]
    elif value.endswith("GB"):
        unit = 1 << 30
        value = value[:-2]
    elif value.endswith("TB"):
        unit = 1 << 40
        value = value[:-2]
    elif value.endswith("PB"):
        unit = 1 << 50
        value = value[:-2]
    try:
        return int(value) * unit
    except ValueError:
        raise ArgumentTypeError(f"{value} is not a valid file size!")


def create_filter(args) -> Filter:
    arguments = {
        "symlink": args.symlink
    }
    if args.ignore_prefix is not None:
        arguments["ignore_prefix"] = args.ignore_prefix
    if args.ignore_suffix is not None:
        arguments["ignore_suffix"] = args.ignore_suffix
    if args.max_size is not None:
        arguments["max_size"] = args.max_size
    if args.min_size is not None:
        arguments["min_size"] = args.min_size
    if args.regex is not None:
        arguments["regex"] = args.regex
    return Filter(**arguments)


if __name__ == "__main__":
    main()
