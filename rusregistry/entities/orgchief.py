from entities.entity import ConnectionEntity
import pandas as pd
from csv_processing.utils import fix_inn

class OrgChief(ConnectionEntity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Directorship'

    def from_csv_row(self, row: pd.core.series.Series):
        row['inn'] = fix_inn(row['inn'])
        row['chief_inn'] = fix_inn(row['chief_inn'])

        row = self.fix_date(row)
        self.data_dict = {'director': str(row['chief_inn']),
                          'organization': str(row['ogrn']),
                          'role': row['chief_position'],
                          'startDate': row['cdate_num']}

    def make_id(self, entity):
        entity.id = self.data_dict['director'] + 'orgChief' + self.data_dict['organization']
        return entity
