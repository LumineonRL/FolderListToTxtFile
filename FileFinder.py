"""
This module contains a class 'FileFinder' which is used to find files in specified directories,
filter them based on extensions and save filtered paths of all files found in those directories 
to a text file.
"""

import os
import glob
from datetime import datetime
from typing import List


class FileFinder:
    def __init__(
        self,
        extensions_to_check: List[str],
        input_paths_file: str,
        output_path_file: str,
        file_prefix: str,
        encoding: str,
    ) -> None:
        self.input_paths_file = input_paths_file
        self.output_path_file = output_path_file
        self.encoding = encoding
        self.extensions_to_check = extensions_to_check
        self.file_prefix = file_prefix

    def get_input_directories(self) -> List[str]:
        with open(self.input_paths_file, "r", encoding=self.encoding) as input_file:
            input_directories = [line.strip() for line in input_file]

        return input_directories

    def get_output_directory(self) -> str:
        with open(self.output_path_file, "r", encoding=self.encoding) as output_file:
            output_directory = output_file.readline().strip()

        return output_directory

    def write_files_paths_to_txt(
        self, input_directories: List[str], output_directory: str
    ) -> None:
        all_files_in_directories_list = self._find_all_files_in_directories(
            input_directories
        )
        filtered_valid_extensions_list = self._filter_valid_extensions_from_all(
            all_files_in_directories_list
        )

        if len(filtered_valid_extensions_list) > 0:
            filename_with_timestamp = (
                self._generate_filename_with_timestamp_and_prefix()
            )
            filepath = os.path.join(output_directory, filename_with_timestamp)

            self._write_list_to_txt(filtered_valid_extensions_list, filepath)

        else:
            print("No files found.")

    def _find_all_files_in_directories(self, input_directories: List[str]) -> List[str]:
        files = []

        for dir_path in input_directories:
            dir_files = glob.glob(os.path.join(dir_path, "**/*"), recursive=True)
            files.extend(dir_files)

        return files

    def _filter_valid_extensions_from_all(self, file_paths: List[str]) -> List[str]:
        return [path for path in file_paths if self._is_extension_in_list(path)]

    def _is_extension_in_list(self, extension: str) -> bool:
        _, ext = os.path.splitext(extension)

        return ext.lower() in self.extensions_to_check

    def _generate_filename_with_timestamp_and_prefix(self) -> str:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        return f"{self.file_prefix}{timestamp_str}.txt"

    def _write_list_to_txt(self, filelist: List[str], output_file_path: str) -> None:
        with open(output_file_path, "w", encoding=self.encoding) as output_file:
            for item in filelist:
                output_file.write(f"{item}\n")
