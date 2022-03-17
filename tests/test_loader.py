from unittest import TestCase

import mongoengine as me

from etl.loader import Loader
from etl.models import CakeMongoOrm, CakeModel



class TestLoader(TestCase):
    """
    Test Loader
    """

    @classmethod
    def setUpClass(cls):
        me.connect('caketest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
       me.disconnect()
      
    def test_load_data(self):
        '''Assert loader works properly'''

        cake_data = [
            CakeModel(
                entry_id=180, 
                diameter_in_mm=522, 
                name='cream', 
                original_unit='mm', 
                vegan=False
            ),
            CakeModel(
                entry_id=201,
                diameter_in_mm=400,
                name='strawberry',
                original_unit='mm',
                vegan=True
            )
        ]
    
        loader = Loader(cake_data, test_mode=True)
        loader.load_data()
        cake_count = CakeMongoOrm.objects().count()

        cake = CakeMongoOrm.objects(entry_id=cake_data[0].entry_id).first()

        self.assertEqual(len(cake_data), cake_count)

        self.assertEqual(cake_data[0].original_unit, cake.original_unit)
        self.assertEqual(cake_data[0].diameter_in_mm, cake.diameter_in_mm)
        self.assertEqual(cake_data[0].entry_id, cake.entry_id)
        self.assertEqual(cake_data[0].name, cake.name)
        self.assertEqual(cake_data[0].vegan, cake.vegan)