from entities.entity import ConnectionEntity
import pandas as pd

class Succession(ConnectionEntity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Succession'



    def from_csv_row(self, row: pd.core.series.Series):
        row = self.fix_date(row)
        predecessor_id = self.add_id_prefix(row['predecessor_ogrn'], 'ogrn')
        sucessor_id = self.add_id_prefix(row['ogrn'], 'ogrn')

        self.data_dict = {'predecessor': predecessor_id,
                          'successor': sucessor_id,
                          'date': row['cdate_num']}

    def make_id(self, entity):
        entity.id = f"{self.data_dict['successor']}-sucessor-{self.data_dict['predecessor']}"
        return entity
