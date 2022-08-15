from entities.entity import Entity
import pandas as pd

class SupportTransaction(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Payment'

    def from_csv_row(self, row: pd.core.series.Series):
        description = f"Type: {row['type']}, Form: {row['form']}"
        self.data_dict = {'beneficiary': row['inn'],
                          'payer': row['from_inn'],
                          'date': row['accept_date'],
                          'amount': row['s'],
                          'description': description}

    def make_id(self, entity):
        entity.id = self.data_dict['payer'] + 'transaction' + self.data_dict['beneficiary']
        return entity
