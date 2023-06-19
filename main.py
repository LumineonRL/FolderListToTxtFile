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
    my_finder = instantiate_finder(my_args)
    write_files(my_finder)
