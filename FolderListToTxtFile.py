import os
import glob
from datetime import datetime


class FileFinder:
    def __init__(
        self,
        extensions_to_check: list[str],
        input_paths_file: str,
        output_path_file: str,
    ):
        self.input_paths_file = input_paths_file
        self.output_path_file = output_path_file
        self.encoding = "utf-8"
        self.extensions_to_check = extensions_to_check

    def get_input_dirs(self) -> list[str]:
        """Reads in list of input directories from InputPaths file"""
        with open(self.input_paths_file, "r", encoding=self.encoding) as f:
            input_dirs = [line.strip() for line in f]
        return input_dirs

    def get_output_dir(self) -> str:
        """Reads in output directory path from OutputPath file"""
        with open(self.output_path_file, "r", encoding=self.encoding) as f:
            output_dir = f.readline().strip()
        return output_dir

    def write_files_paths_to_txt_file(
        self, input_dirs: list[str], extensions_to_check: list[str], output_dir: str
    ) -> None:
        """Generates an appropriate name for the textfile based on current date/time and calls another
        function to actually save paths into this newly generated textfile."""

        filtered_paths = self.find_files_with_extensions_in_directories(
            input_dirs=input_dirs
        )

        if len(filtered_paths) > 0:
            output_filename = self.generate_output_filename_with_timestamp()
            output_filepath = os.path.join(output_dir, output_filename)

            self.write_list_to_file(filtered_paths, output_filepath)
        else:
            print("No files found.")

    def find_files_with_extensions_in_directories(
        self, input_dirs: list[str]
    ) -> list[str]:
        """Finds all files with specified extensions recursively within given directories."""
        files = []
        for dir_path in input_dirs:
            files.extend(glob.glob(os.path.join(dir_path, "**/*"), recursive=True))
        files_filtered_by_extensions = self.get_files_with_specified_extensions(files)

        return files_filtered_by_extensions

    def get_files_with_specified_extensions(
        self, files_list: list[str] = []
    ) -> list[str]:
        """Returns a list containing all files with an extension that matches one or more of the specified extensions."""
        files_filtered = [
            path for path in files_list if self.is_file_of_specified_extension(path)
        ]

        return files_filtered

    def is_file_of_specified_extension(self, file_path: str) -> bool:
        """Checks if a given file has an extension that matches one or more of the specified extensions."""
        file_extension = os.path.splitext(file_path)[-1].lower()
        if file_extension in self.extensions_to_check:
            return True
        else:
            return False

    def generate_output_filename_with_timestamp(self) -> str:
        """Returns an output filename with timestamp appended"""
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        return "files_" + timestamp_str + ".txt"

    def write_list_to_file(self, file_list: list[str], output_path: str) -> None:
        """Writes a list of strings to a txt file at the specified output path."""
        with open(output_path, "w", encoding=self.encoding) as f:
            for item in file_list:
                encoded_item = item.encode(self.encoding)
                decoded_item = encoded_item.decode(self.encoding)

                # Finally write the decoded string onto our desired txt-file.
                f.write("%s\n" % decoded_item)


if __name__ == "__main__":
    extensions = [".jpg", ".jpeg", ".png", ".gif", ".webm"]
    input_path_file = "InputPaths.txt"
    output_path_file = "OutputPath.txt"

    finder = FileFinder(
        extensions_to_check=extensions,
        input_paths_file=input_path_file,
        output_path_file=output_path_file,
    )

    input_dirs = finder.get_input_dirs()
    output_dir = finder.get_output_dir()

    finder.write_files_paths_to_txt_file(
        input_dirs=input_dirs, extensions_to_check=extensions, output_dir=output_dir
    )
