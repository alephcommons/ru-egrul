import pandas as pd
import random
import string
from typing import List, Dict
import followthemoney as ftm

def get_unique_id():
    # This should be fixed
    return ''.join(random.sample(string.ascii_letters, 24))

class Entity:
    def __init__(self, item):
        self.entity_type = None
        if type(item) == pd.core.series.Series:
            self.from_csv_row(item.copy())
        else:
            raise TypeError("Unrecognised input type! Currently supported types: [pd.Series]")

    def from_csv_row(self, row: pd.core.series.Series):
        self.data_dict = row.to_dict()

    def add_id_prefix(self, item_id, prefix='ogrn'):
        return f"ru-{prefix}-{item_id}"

    def make_id(self, entity):
        entity.id = self.add_id_prefix(get_unique_id(), 'other')
        return entity

    def set_property(self, property_name, property_value):
        self.data_dict[property_name] = property_value

    def to_ftm(self):
        # TODO return enity as FTM object
        entity = ftm.model.make_entity(self.entity_type)
        # Generate (hopefully) unique ID
        entity = self.make_id(entity)
        # Set properties
        for property_name, property_value in self.data_dict.items():
            entity.add(property_name, property_value)
        return entity

    def fix_na(self):
        raise NotImplementedError


from csv_processing.utils import bytes_to_date

class ConnectionEntity(Entity):
    def fix_date(self, row):
        row['cdate_num'] = bytes_to_date(row['cdate_num'])
        return row
