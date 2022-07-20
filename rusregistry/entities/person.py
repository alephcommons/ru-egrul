from entities.entity import Entity, get_unique_id
import pandas as pd


class Person(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Person'

    def from_csv_row(self, row: pd.core.series.Series):
        self.data_dict = row.to_dict()

    def make_id(self, entity):
        entity.id = self.add_id_prefix(self.data_dict['innCode'], 'inn')
        return entity
