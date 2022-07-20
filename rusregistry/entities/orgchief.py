from entities.entity import Entity
import pandas as pd
from csv_processing.utils import fix_inn

class OrgChief(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Directorship'

    def from_csv_row(self, row: pd.core.series.Series):
        self.data_dict = {'director': row['director_id'],
                          'organization': row['organization_id'],
                          'role': row['chief_position'],
                          'startDate': row['startDate']}

    def make_id(self, entity):
        entity.id = f"{self.data_dict['director']}-orgchief-{self.data_dict['organization']}"
        return entity
