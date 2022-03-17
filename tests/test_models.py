from unittest import TestCase

import mongoengine as me

from etl.models import CakeMongoOrm, CakeModel


class TestCakeModel(TestCase):
    """
    Test Pydantic model of a cake used for data validation
    """

    def test_data_validation(self):
        '''Assert that well formed data is consumed as expected'''

        transformed_data = {
            'original_unit': 'mm',
            'diameter_in_mm': '440.2',
            'entry_id': '234',
            'name': None,
            'vegan': True
        }
        cake_model = CakeModel(**transformed_data)
    
        self.assertEqual(transformed_data['original_unit'], cake_model.original_unit)
        self.assertEqual(float(transformed_data['diameter_in_mm']), cake_model.diameter_in_mm)
        self.assertEqual(int(transformed_data['entry_id']), cake_model.entry_id)
        self.assertIsNone(transformed_data['name'], cake_model.name)
        self.assertTrue(cake_model.vegan)


class TestCakeMongoOrm(TestCase):
    """
    Test Mongoengine model of Cake document
    """

    @classmethod
    def setUpClass(cls):
        me.connect('caketest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
       me.disconnect()

    def test_object_creation(self):
        '''Assert data is created properply'''

        data = {
            'original_unit': 'mm',
            'diameter_in_mm': '440.2',
            'entry_id': '234',
            'name': 'strawberry',
            'vegan': True
        }
        validated_data = CakeModel(**data)
        CakeMongoOrm(**validated_data.dict()).save()
        cake = CakeMongoOrm.objects(entry_id=234).first()

        self.assertEqual(validated_data.original_unit, cake.original_unit)
        self.assertEqual(validated_data.diameter_in_mm, cake.diameter_in_mm)
        self.assertEqual(validated_data.entry_id, cake.entry_id)
        self.assertEqual(validated_data.name, cake.name)
        self.assertEqual(validated_data.vegan, cake.vegan)
      
    def test_bulk_object_creation(self):
        '''Assert bulk data creation works properly'''
        
        bulk_data = [
            {
                'diameter_in_mm': '514.2',
                'entry_id': '200',
                'name': 'cream',
                'original_unit': 'mm',
                'vegan': False
            },
            {
                'diameter_in_mm': '402',
                'entry_id': '201',
                'name': 'strawberry',
                'original_unit': 'mm',
                'vegan': True
            },      
        ]
        bulk_validated_data = [CakeModel(**data).dict() for data in bulk_data]
        cakes = [CakeMongoOrm(**data) for data in bulk_validated_data]
        CakeMongoOrm.objects.insert(cakes)
        cake_count = CakeMongoOrm.objects().count()

        self.assertEqual(len(bulk_validated_data), cake_count)