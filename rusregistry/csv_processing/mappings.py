# Mapping from CSV column naming to FTM property names

COMPANY_MAPPING = {
 'ogrn': "ogrnCode",
 'reg_date': "incorporationDate",
 'end_date': "dissolutionDate",
 'opf_id': "okopfCode",
 'okved_id': "okvedCode",
 'inn': "innCode",
 'kpp': "kppCode",
 'full_name': "name",
 'email': "email",
 'pfr': "pfrNumber",
 'fss': "fssCode",
 'capital': "capital",
 'jurisdiction': 'jurisdiction'
 }

LOCATION_MAPPING = {
 'index': 'postalCode',
 'region': 'region',
 'area': 'state',
 'city': 'city',
 'street': 'street',
 'full': 'full'
}

IE_MAPPING = {
    'inn': "innCode",
    'name': 'name',
    'reg_date':  "incorporationDate",
    'status': 'status',
    'end_date': 'dissolutionDate',
    'okved_id': "okvedCode",
    'tax_office_id': 'taxNumber',
    'email': 'email',
    'pfr': "pfrNumber",
    'fss': "fssCode",
    'country_code': 'jurisdiction',
    'ogrnip': 'ogrnCode',
}

PERSONS_MAPPING = {
    'inn': "innCode",
    'last_name': 'lastName',
    'name': 'firstName',
    'patronymic': 'fatherName',
    'sex': 'gender',
    'email': 'email',
    'country_code': 'country',
    'full_name': "name"
}
