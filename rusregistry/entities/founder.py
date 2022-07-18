from entities.entity import Entity
import pandas as pd
from csv_processing.utils import fix_inn

class Founder(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Ownership'

    def from_csv_row(self, row: pd.core.series.Series):
        self.data_dict = {'owner': row['owner_id'],
                          'asset': row['asset_id'],
                          'percentage': row['capital_p'],
                          'sharesValue': row['capital'],
                          'startDate': row['cdate_num']}

    def make_id(self, entity):
        entity.id = f"{self.data_dict['owner']}-founder-{self.data_dict['asset']}"
        return entity
