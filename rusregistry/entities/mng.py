from entities.entity import ConnectionEntity
import pandas as pd

class ManagingCompany(ConnectionEntity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Directorship'

    def from_csv_row(self, row: pd.core.series.Series):
        row = self.fix_date(row)

        director_id = self.add_id_prefix(row['mng_ogrn'], 'ogrn')
        organisation_id = self.add_id_prefix(row['ogrn'], 'ogrn')

        self.data_dict = {'director': director_id,
                          'organization': organisation_id,
                          'role': 'Managing Company',
                          'startDate': row['cdate_num']}

    def make_id(self, entity):
        entity.id = f"{self.data_dict['director']}-mng-{self.data_dict['organization']}"
        return entity
