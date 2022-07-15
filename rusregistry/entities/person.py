from entities.entity import Entity, get_unique_id
from utils.column_mapping import PERSONS_MAPPING
import pandas as pd
from csv_processing.utils import fix_inn


class Person(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Person'

    def update_column_names(self, row: pd.core.series.Series):
        row['full_name'] =  f"{row['last_name']} {row['name']} {row['patronymic']}"
        return row.rename(PERSONS_MAPPING, axis=0)

    def from_csv_row(self, row: pd.core.series.Series):
        row = self.fix_na(row)
        row['ogrnip'] = str(row['ogrnip'])
        row['inn'] = fix_inn(row['inn'])

        row = self.update_column_names(row.copy())
        row = row[PERSONS_MAPPING.values()]
        self.data_dict = row.to_dict()

    def fix_na(self, row):
        row['pfr'] = None if row['pfr'] == 0 else row['pfr']
        row['fss'] = None if row['fss'] == 0 else row['fss']
        return row

    def make_id(self, entity):
        entity.id = self.add_id_prefix(self.data_dict['innCode'], 'inn')
        return entity
