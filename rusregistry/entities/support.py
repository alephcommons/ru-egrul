from csv_processing.utils import fix_inn
from entities.entity import Entity

class Support(Entity):
    def __init__(self, item):
        super().__init__(item)
        self.entity_type = 'Debt'

    def from_csv_row(self, row: pd.core.series.Series):
        description = f"Type: {row['type']}, Form: {row['form']}"
        debtor_id = fix_inn(row['inn'])
        creditor_id = fix_inn(row['inn'])
        self.data_dict = {'debtor': debtor_id,
                          'creditor': creditor_id,
                          'startDate': row['accept_date'],
                          'endDate': row['end_date'],
                          'amount': row['s'],
                          'description': description}

    def make_id(self, entity):
        entity.id = self.data_dict['debtor'] + 'debtFrom' + self.data_dict['creditor']
        return entity
