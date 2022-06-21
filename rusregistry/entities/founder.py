from entities.entity import ConnectionEntity
import pandas as pd
from csv_processing.utils import fix_inn

class Founder(ConnectionEntity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Ownership'

    def from_csv_row(self, row: pd.core.series.Series):
        row['inn'] = fix_inn(row['inn'])
        row['founder_inn'] = fix_inn(row['founder_inn'])


        founder = str(row['founder_inn'] if row['founder_ogrn'] == 0 else row['founder_ogrn'])
        row = self.fix_date(row)


        self.data_dict = {'owner': founder,
                          'asset': str(row['ogrn']),
                          'percentage': row['capital_p'],
                          'sharesValue': row['capital'],
                          'startDate': row['cdate_num']}

    def make_id(self, entity):
        entity.id = self.data_dict['owner'] + 'founder' + self.data_dict['asset']
        return entity
