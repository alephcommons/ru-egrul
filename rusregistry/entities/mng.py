from entities.entity import Entity
import pandas as pd

class ManagingCompany(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Directorship'

    def from_csv_row(self, row: pd.core.series.Series):
        self.data_dict = {'director': row['director_id'],
                          'organization': row['organization_id'],
                          'role': 'Managing Company',
                          'startDate': row['startDate']}

    def make_id(self, entity):
        entity.id = f"{self.data_dict['director']}-mng-{self.data_dict['organization']}"
        return entity
