from entities.entity import ConnectionEntity
import pandas as pd

class ManagingCompany(ConnectionEntity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Directorship'

    def from_csv_row(self, row: pd.core.series.Series):
        row = self.fix_date(row)
        self.data_dict = {'director': str(row['mng_ogrn']),
                          'organization': str(row['ogrn']),
                          'role': 'Managing Company',
                          'startDate': row['cdate_num']}

    def make_id(self, entity):
        entity.id = self.data_dict['director'] + 'mng' + self.data_dict['organization']
        return entity
