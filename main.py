import argparse
from FileFinder import FileFinder


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("output_file", help="Path to output file")
    parser.add_argument(
        "extensions",
        nargs="+",
        help="List of extensions to check (e.g. .jpg .jpeg .png)",
    )

    parser.add_argument(
        "--file_prefix",
        default="files_",
        help="Prefix for output files (default is 'files_')",
    )

    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Encoding format for input and output files (default is utf-8)",
    )

    return parser.parse_args()

def run_validation(args: argparse.Namespace) -> None:
    if not validate_encoding(args.encoding):
        print(f"{args.encoding} is NOT a valid codec name.")


def validate_encoding(encoding_to_validate: str) -> bool:
    valid_encodings = [
        "ascii",
        "big5",
        "big5hkscs",
        "cp037",
        "cp273",
        "cp424",
        "cp437",
        "cp500",
        "cp720",
        "cp737",
        "cp775",
        "cp850",
        "cp852",
        "cp855",
        "cp856",
        "cp857",
        "cp858",
        "cp860",
        "cp861",
        "cp862",
        "cp863",
        "cp864",
        "cp865",
        "cp866",
        "cp869",
        "cp874",
        "cp875",
        "cp932",
        "cp949",
        "cp950",
        "cp1006",
        "cp1026",
        "cp1125",
        "cp1140",
        "cp1250",
        "cp1251",
        "cp1252",
        "cp1253",
        "cp1254",
        "cp1255",
        "cp1256",
        "cp1257",
        "cp1258",
        "euc-jp",
        "euc-jis-2004",
        "euc-jisx0213",
        "euc-kr",
        "gb2312",
        "gbk",
        "gb18030",
        "hz",
        "iso2022-jp",
        "iso2022-jp-1",
        "iso2022-jp-2",
        "iso2022-jp-2004",
        "iso2022-jp-3",
        "iso2022-jp-ext",
        "iso2022-kr",
        "latin-1",
        "iso8859-2",
        "iso8859-3",
        "iso8859-4",
        "iso8859-5",
        "iso8859-6",
        "iso8859-7",
        "iso8859-8",
        "iso8859-9",
        "iso8859-10",
        "iso8859-11",
        "iso8859-13",
        "iso8859-14",
        "iso8859-15",
        "iso8859-16",
        "johab",
        "koi8-r",
        "koi8-t",
        "koi8-u",
        "kz1048",
        "mac-cyrillic",
        "mac-greek",
        "mac-iceland",
        "mac-latin2",
        "mac-roman",
        "mac-turkish",
        "ptcp154",
        "shift-jis",
        "shift-jis-2004",
        "shift-jisx0213",
        "utf-32",
        "utf-32-be",
        "utf-32-le",
        "utf-16",
        "utf-16-be",
        "utf-16-le",
        "utf-7",
        "utf-8",
        "utf-8-sig",
    ]

    return encoding_to_validate in valid_encodings


def instantiate_finder(args: argparse.Namespace) -> FileFinder:
    return FileFinder(
        extensions_to_check=args.extensions,
        input_paths_file=args.input_file,
        output_path_file=args.output_file,
        file_prefix=args.file_prefix,
        encoding=args.encoding,
    )


def write_files(finder: FileFinder):
    my_input_directories = finder.get_input_directories()
    my_output_directory = finder.get_output_directory()

    try:
        finder.write_files_paths_to_txt(my_input_directories, my_output_directory)

    except FileNotFoundError as e:
        print(f"ERROR: {e.filename} not found.")


if __name__ == "__main__":
    my_args = parse_arguments()
    run_validation(my_args)
    my_finder = instantiate_finder(my_args)
    write_files(my_finder)
