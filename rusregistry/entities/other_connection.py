from entities.entity import Entity
import pandas as pd

class OtherConnection(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'UnknownLink'

    def from_csv_row(self, row: pd.core.series.Series):
        description = f"Type: {row['type']}, Form: {row['form']}, Sum: {row['s']}"
        self.data_dict = {'object': row['inn'],
                          'subject': row['from_inn'],
                          'date': row['accept_date'],
                          'description': description}

    def make_id(self, entity):
        entity.id = self.data_dict['object'] + 'support' + self.data_dict['subject']
        return entity
