import csv

from typing import List


class Extractor:
    def __init__(self, in_file_path: str):
        """
        This class extracts data from source file

        Args:
            in_file_path: path to the source file
        """
        self.in_file_path = in_file_path

    def extract_data(self) -> List[dict]:
        """
        Extracts data from CSV file

        Returns:
            data as a list of dictionaries
        """

        with open(self.in_file_path, "r") as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            next(reader)
            return list(reader)