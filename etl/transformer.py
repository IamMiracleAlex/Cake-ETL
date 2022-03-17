from string import punctuation
from typing import List, Optional

from .models import CakeModel
from .utils import split_text, get_base_unit, is_number, value_to_mm


class Transformer:
    def __init__(self, raw_data: List[dict]):
        """
        This class transforms extracted data according to the desired model

        Args:
            raw_data: extracted data
        """
        self.raw_data = raw_data

    def transform_data(self) -> List[CakeModel]:
        """
        Transforms data

        Returns:
            transformed data as a list of models
        """
        transformed_cakes = list()
        for in_cake in self.raw_data:
            out_cake = self.transform_single_item(in_cake)
            if out_cake:
                transformed_cakes.append(out_cake)
        return transformed_cakes

    def transform_single_item(self, input_item: dict) -> Optional[CakeModel]:
        """
        Transforms single item of extracted data

        Args:
            input_item: part of extracted data

        Returns:
            model if transformation was successful
        """

        original_unit, diameter = self.process_diameter(
                            unit=input_item.get('diam_unit'), 
                            diameter=input_item.get('cake_diameter')
                        )

        new = {
            'original_unit': original_unit,
            'diameter_in_mm': diameter,
            'entry_id': input_item.get('entry'),
            'name': self.process_name(input_item.get('flavor')),
            'vegan': self.process_vegan(input_item.get('is_cake_vegan')),
        }
     
        return CakeModel(**new) if diameter and original_unit else None


    def process_diameter(self, unit, diameter):
        '''
        Process the unit and diameter
        
        Args:
            unit: the diameter unit
            diameter: the diameter

        Returns:
            original unit and processed diameter
        '''
     
        NON_MM_UNITS = ['in', 'm']
        diameter = diameter.strip().lower()
        unit = unit.strip().lower()

        # when no units are mentioned, set to milimeters
        if unit in ['', '"']:
            unit = 'mm'

        # get diamter value
        # if diameter value is irrecoverable (a complete string), discard
        if diameter[0].isalpha() and diameter[-1].isalpha():
            return None, None

        # if diameter has units, split into diameter and units
        elif diameter[-1].isalpha():
            diameter_detials = list(split_text(diameter))
           
            # if units doesn't match, discard record
            if get_base_unit(unit) != get_base_unit(diameter_detials[1]):
                return None, None

            # if they match, continue
            else:
                # if they're not millimeters, convert
                if get_base_unit(unit) in NON_MM_UNITS:
                    diameter = value_to_mm(value=float(diameter_detials[0]), unit=get_base_unit(unit))

                # if they're in millimeters, return diameter
                else:
                    diameter = diameter_detials[0]

        # check case diameter is in the form '2.43"' convert to ['2.43', ''] 
        elif diameter[-1] in punctuation:
            diameter_detials = diameter.split(diameter[-1])
            diameter = diameter_detials[0]
            
        # when diameter has no units
        else:
            # check if unit is in millimeters, else convert
            if get_base_unit(unit) in NON_MM_UNITS:
                diameter = value_to_mm(value=float(diameter), unit=get_base_unit(unit))

            
        return get_base_unit(unit), diameter

    
    def process_name(self, value):
        '''
        Process and return desired cake flavor

        Args:
            value: the flavour of cake

        Returns:
            the accepted flavour or name if it exists
        '''
        from etl import models

        value = value.strip().lower()
        return  value if value in models.VALID_CAKE_FLAVORS else None
      

    def process_vegan(self, value):
        '''
        Process and return desired vegan value

        Args:
            value: the vegan value

        Returns:
            True or False if vegan value exists
        '''

        value = value.strip().lower()
        if value in ['t','true', 'y', 'yes']:
            return True
        elif value in ['f', 'false', 'n', 'no']:
            return False
        elif is_number(value): 
            return bool(float(value))
        return None