from pathlib import Path
from unittest.case import TestCase

from etl.reports import Report


class TestReport(TestCase):
    """
    Test Report
    """

    def setUp(self):

        self.data = [
            {
                'entry_id': 58, 
                'name': None, 
                'diameter_in_mm': 534900.0, 
                'vegan': False, 
                'original_unit': 'm'
            }, 
            {
                'entry_id': 60, 
                'name': None, 
                'diameter_in_mm': 556.2, 
                'vegan': True, 
                'original_unit': 'mm'
            }
        ]

    def test_report_is_generated(self):
        '''Assert that report are generated'''

        path = './reports/test_reports.html'
        report = Report(
            data=self.data,
            caption='Test Reports (created from unit test)',
            path=path
        )
        report.create_report()
        new_file = Path(path).resolve()

        self.assertEqual(new_file.is_file(), True)