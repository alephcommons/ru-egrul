from entities.entity import Entity, get_unique_id
import pandas as pd


class Address(Entity):
    def __init__(self, item):
        self.properties = ['full', 'postalCode', 'region', 'state', 'city', 'street']
        super().__init__(item)
        self.entity_type = 'Address'

    def from_csv_row(self, row: pd.core.series.Series):
        row = row[self.properties]
        self.data_dict = row.to_dict()

    def make_id(self, entity):
        entity.id = self.add_id_prefix(get_unique_id(), 'address')
        return entity
