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


        founder_id = self.add_id_prefix(row['founder_inn'], 'inn') if row['founder_ogrn'] == 0 \
                                     else self.add_id_prefix(row['founder_ogrn'], 'ogrn')
        row = self.fix_date(row)
        asset_id = self.add_id_prefix(row['ogrn'], 'ogrn')
        self.data_dict = {'owner': founder_id,
                          'asset': asset_id,
                          'percentage': row['capital_p'],
                          'sharesValue': row['capital'],
                          'startDate': row['cdate_num']}

    def make_id(self, entity):
        entity.id = f"{self.data_dict['owner']}-founder-{self.data_dict['asset']}"
        return entity
