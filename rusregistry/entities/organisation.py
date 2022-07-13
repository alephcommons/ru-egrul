from entities.entity import Entity, get_unique_id
from utils.column_mapping import COMPANY_MAPPING
import pandas as pd
from csv_processing.utils import fix_inn


class Organisation(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Company'

    def update_column_names(self, row: pd.core.series.Series):
        return row.rename(COMPANY_MAPPING, axis=0)

    def from_csv_row(self, row: pd.core.series.Series):
        row = self.fix_na(row)
        row['ogrn'] = str(row['ogrn'])
        row['inn'] = fix_inn(row['inn'])

        row = row[COMPANY_MAPPING.keys()]
        row = self.update_column_names(row)
        self.data_dict = row.to_dict()

    def make_id(self, entity):
        entity.id = self.add_id_prefix(self.data_dict['ogrnCode'], 'ogrn')
        return entity

    def fix_na(self, row):
        row['end_date'] = None if row['end_date'] == '0000-00-00' else row['end_date']
        row['pfr'] = None if row['pfr'] == 0 else row['pfr']
        row['fss'] = None if row['fss'] == 0 else row['fss']
        return row
