from entities.entity import Entity, get_unique_id
from utils.column_mapping import LOCATION_MAPPING
import pandas as pd


class Address(Entity):
    def __init__(self, item):
        self.full_address_columns = ['region', 'area','city', 'street', 'house', 'corpus', 'apartment']
        self.properties = ['full', 'postalCode', 'region', 'state', 'city', 'street']
        super().__init__(item)
        self.entity_type = 'Address'

    def update_column_names(self, row: pd.core.series.Series):
        row['full'] = ' '.join(row[self.full_address_columns].apply(str).values)
        return row.rename(LOCATION_MAPPING, axis=0)

    def from_csv_row(self, row: pd.core.series.Series):
        # row = self.fix_na(row)
        row = self.update_column_names(row)
        row = row[self.properties]
        self.data_dict = row.to_dict()

    def make_id(self, entity):
        entity.id = self.add_id_prefix(get_unique_id(), 'address')
        return entity
