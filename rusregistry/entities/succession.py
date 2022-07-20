from entities.entity import Entity
import pandas as pd

class Succession(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Succession'

    def from_csv_row(self, row: pd.core.series.Series):
        self.data_dict = {'predecessor': row['predecessor_id'],
                          'successor': row['sucessor_id'],
                          'date': row['date']}

    def make_id(self, entity):
        entity.id = f"{self.data_dict['successor']}-sucessor-{self.data_dict['predecessor']}"
        return entity
