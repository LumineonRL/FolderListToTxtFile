import os
import glob
from datetime import datetime


class FileFinder:
    def __init__(
        self,
        extensions_to_check: list[str],
        input_paths_file: str,
        output_path_file: str,
        file_prefix: str
    ):
        self.input_paths_file = input_paths_file
        self.output_path_file = output_path_file
        self.encoding = "utf-8"
        self.extensions_to_check = extensions_to_check
        self.file_prefix = file_prefix

    def get_input_dirs(self) -> list[str]:
        with open(self.input_paths_file, "r", encoding=self.encoding) as f:
            input_dirs = [line.strip() for line in f]
        return input_dirs

    def get_output_dir(self) -> str:
        with open(self.output_path_file, "r", encoding=self.encoding) as f:
            output_dir = f.readline().strip()
        return output_dir

    def write_files_paths_to_txt_file(
        self, input_dirs: list[str], extensions_to_check: list[str], output_dir: str
    ) -> None:
        all_file_paths = self._find_all_files_in_directories(input_dirs)
        filtered_paths = self._filter_valid_file_extensions(all_file_paths)

        if len(filtered_paths) > 0:
            output_filename = self._generate_output_filename_with_timestamp()
            output_filepath = os.path.join(output_dir, output_filename)

            self._write_list_to_file(filtered_paths, output_filepath)
        else:
            print("No files found.")

    def _find_all_files_in_directories(self, input_dirs: list[str]) -> list[str]:
        files = []

        for dir_path in input_dirs:
            dir_files = glob.glob(os.path.join(dir_path, "**/*"), recursive=True)
            files.extend(dir_files)

        return files

    def _filter_valid_file_extensions(self, file_paths: list[str]) -> list[str]:
        valid_files = [f for f in file_paths if self._is_file_of_specified_extension(f)]

        return valid_files

    def _is_file_of_specified_extension(self, file_path: str) -> bool:
        ext = self._get_file_extension(file_path)
        result = self._is_extension_in_list(ext)

        return result

    def _get_file_extension(self, file_path):
        """
        Returns the extension of a file (including . separator) as a string.
        """
        _, ext = os.path.splitext(file_path)

        return ext.lower()

    def _is_extension_in_list(self, extension):
        return extension in self.extensions_to_check

    def _generate_output_filename_with_timestamp(self) -> str:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return f"{self.file_prefix}{timestamp_str}.txt" 

    def _write_list_to_file(self, file_list: list[str], output_path: str) -> None:
        with open(output_path, "w", encoding=self.encoding) as f:
            for item in file_list:
                encoded_item = item.encode(self.encoding)
                decoded_item = encoded_item.decode(self.encoding)

                f.write("%s\n" % decoded_item)


if __name__ == "__main__":
    extensions = [".jpg", ".jpeg", ".png", ".gif", ".webm"]
    input_path_file = "InputPaths.txt"
    output_path_file = "OutputPath.txt"
    file_prefix = "files_"

    finder = FileFinder(
        extensions_to_check=extensions,
        input_paths_file=input_path_file,
        output_path_file=output_path_file,
        file_prefix=file_prefix
    )

    input_dirs = finder.get_input_dirs()
    output_dir = finder.get_output_dir()

    finder.write_files_paths_to_txt_file(
        input_dirs=input_dirs, extensions_to_check=extensions, output_dir=output_dir
    )