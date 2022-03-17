from unittest.case import TestCase

from etl.extractor import Extractor


class TestExtractor(TestCase):
    """
    Test Extractor
    """

    def test_extractor(self):
        '''Assert data is extracted properly'''

        file_path = './cake_data.csv'
        extractor = Extractor(in_file_path=file_path)
        data = extractor.extract_data()

        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
        self.assertEqual(len(data[0]), 5)
        self.assertIsNotNone(data[0].get('entry'))
