from typing import List

import mongoengine as me

from .models import CakeModel, CakeMongoOrm


def connect():
    """
    Connects to the database
    """
    me.connect("cakes")
    

class Loader:
    def __init__(self, cake_data: List[CakeModel], test_mode: bool = False):
        """
        This class loads transformed data into the database

        Args:
            cake_data: transformed data
            test_mode: live mode or unit testing mode
        """

        if not test_mode:
            connect()
            
        self.cake_data = cake_data

    def load_data(self):
        """
        Inserts data into the database
        """

        print("Preparing data...")
        cakes = [CakeMongoOrm(**data.dict()) for data in self.cake_data]
        
        CakeMongoOrm.objects.delete()

        print("Inserting data into the database... please wait")
        CakeMongoOrm.objects.insert(cakes)

        print("Data loaded into the database successfully!")
