from unittest.case import TestCase

from etl.transformer import Transformer


class TestTransformer(TestCase):
    """
    Test Transformer
    """

    def test_transformer_valid_unit_mm(self):
        '''Assert that transformer converts properly'''

        transformer = Transformer(
            raw_data=[
                {
                    "entry": "1",
                    "cake_diameter": "56.78",
                    "diam_unit": "mm",
                    "flavor": "caramel",
                    "is_cake_vegan": "No",
                }
            ]
        )
        res = transformer.transform_data()[0]

        self.assertEqual(res.entry_id, 1)
        self.assertEqual(res.name, "caramel")
        self.assertEqual(res.diameter_in_mm, 56.78)
        self.assertFalse(res.vegan)
        self.assertEqual(res.original_unit, "mm")

    def test_diameter_conversion(self):
        '''Assert diameter in other units converts to mm'''

        transformer = Transformer(
            raw_data=[
                {
                    "entry": "2",
                    "cake_diameter": "5",
                    "diam_unit": "m",
                    "flavor": "strawberry",
                    "is_cake_vegan": "yes",
                }
            ]
        )
        res = transformer.transform_data()[0]

        self.assertEqual(res.entry_id, 2)
        self.assertEqual(res.name, "strawberry")
        self.assertEqual(res.diameter_in_mm, 5000)
        self.assertTrue(res.vegan)
        self.assertEqual(res.original_unit, "m")

    def test_irrecoverable_data_quality(self):
        '''Assert that record is discarded when data quality is irrecoverable'''

        transformer = Transformer(
            raw_data=[
                {
                    "entry": "3",
                    "cake_diameter": "56.78mm",
                    "diam_unit": "in",
                    "flavor": "caramel",
                    "is_cake_vegan": "false",
                },
                {
                    "entry": "4",
                    "cake_diameter": "fill this info later",
                    "diam_unit": "in",
                    "flavor": "caramel",
                    "is_cake_vegan": "true",
                }
            ]
        )
        res = transformer.transform_data()

        self.assertListEqual(res, [])
       
    def test_mixed_diameter_value(self):
        '''Assert diameter is resolved, even when it is in the form `56mm` '''

        transformer = Transformer(
            raw_data=[
                {
                    "entry": "5",
                    "cake_diameter": "56.78mm",
                    "diam_unit": "mm",
                    "flavor": "caramel",
                    "is_cake_vegan": "No",
                }
            ]
        )
        res = transformer.transform_data()[0]

        self.assertEqual(res.entry_id, 5)
        self.assertEqual(res.name, "caramel")
        self.assertEqual(res.diameter_in_mm, 56.78)
        self.assertFalse(res.vegan)
        self.assertEqual(res.original_unit, "mm")
    
    def test_valid_flavor(self):
        '''Assert only valid flavours/name are returned'''

        transformer = Transformer(
            raw_data=[
                {
                    "entry": "6",
                    "cake_diameter": "60",
                    "diam_unit": "mm",
                    "flavor": "Invalid flavour",
                    "is_cake_vegan": "No",
                }
            ]
        )    
        res = transformer.transform_data()[0]

        self.assertEqual(res.entry_id, 6)
        self.assertIsNone(res.name)
        self.assertEqual(res.diameter_in_mm, 60)
        self.assertFalse(res.vegan)
        self.assertEqual(res.original_unit, "mm")

    def test_valid_vegan(self):
        '''Assert that vegan is validated, invalid ones resolves to None'''

        transformer = Transformer(
            raw_data=[
                {
                    "entry": "7",
                    "cake_diameter": "78",
                    "diam_unit": "mm",
                    "flavor": "caramel",
                    "is_cake_vegan": "Invalid Vegan",
                }
            ]
        )    
        res = transformer.transform_data()[0]

        self.assertEqual(res.entry_id, 7)
        self.assertEqual(res.name, 'caramel')
        self.assertEqual(res.diameter_in_mm, 78)
        self.assertIsNone(res.vegan)
        self.assertEqual(res.original_unit, "mm")

    def test_valid_diameter_unit(self):
        '''Assert empty diameter unit defaults to mm'''

        transformer = Transformer(
            raw_data=[
                {
                    "entry": "8",
                    "cake_diameter": "80",
                    "diam_unit": "",
                    "flavor": "caramel",
                    "is_cake_vegan": "y",
                }
            ]
        )        
        res = transformer.transform_data()[0]

        self.assertEqual(res.entry_id, 8)
        self.assertEqual(res.name, 'caramel')
        self.assertEqual(res.diameter_in_mm, 80)
        self.assertTrue(res.vegan)
        self.assertEqual(res.original_unit, "mm")