from entities.entity import ConnectionEntity
import pandas as pd

class Succession(ConnectionEntity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Succession'

    def from_csv_row(self, row: pd.core.series.Series):
        row = self.fix_date(row)
        self.data_dict = {'predecessor': str(row['predecessor_ogrn']),
                          'successor': str(row['ogrn']),
                          'date': row['cdate_num']}

    def make_id(self, entity):
        entity.id = self.data_dict['successor'] + 'sucessor' + self.data_dict['predecessor']
        return entity
