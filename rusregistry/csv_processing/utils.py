from parsel import Selector
import requests
from urllib.parse import urljoin, unquote
import csv_processing.mappings as mapping
from entities.organisation import Organisation
from entities.address import Address
from entities.individual_enterpreneur import IndividualEnterpereneur
from entities.person import Person

def bytes_to_date(d):
    d = int(d)
    year = '20{:02d}'.format(d>>9)
    month = '{:02d}'.format((d>>5)&15)
    day = '{:02d}'.format(d&31)
    return f'{year}-{month}-{day}'

def fix_inn(inn):
    inn = str(inn)
    if len(inn) in {9, 11}:
        return '0'+inn
    return inn


def get_file_links(uri):
        egrul = requests.get(uri)
        sel = Selector(egrul.text)

        return [
            urljoin(uri, unquote(link))
            for link in sel.css("a::attr(href)").extract()
            if link.endswith("zip") or link.endswith("csv")
        ]

def add_id_prefix(item_id, prefix='ogrn'):
    return f"ru-{prefix}-{item_id}"

def preprocess_company(df):
    df = df.rename(mapping.COMPANY_MAPPING, axis=1)

    df = df.sort_values('max_num', ascending=True).drop_duplicates('ogrnCode', keep='last')
    df['innCode'] = df['innCode'].apply(fix_inn)
    df['ogrnCode'] = df['ogrnCode'].apply(str)
    df['jurisdiction'] = 'Russia'
    df['dissolutionDate'] = df['dissolutionDate'].apply(lambda x: None if x == '0000-00-00' else x)
    df['pfrNumber'] = df['pfrNumber'].apply(lambda x: None if x == 0 else x)
    df['fssCode'] = df['fssCode'].apply(lambda x: None if x == 0 else x)
    # Preprocessing for location data
    df = df.rename(mapping.LOCATION_MAPPING, axis=1)
    df['full'] = df.apply(lambda row: f"region: {row['region']}, 'state': {row['state']},\
                                city: {row['city']}, street: {row['street']},\
                                house: {row['house']}, corpus: {row['corpus']},\
                                apartment: {row['apartment']}", axis=1)
    return df

def preprocess_person(df):
    df = df.rename(mapping.PERSONS_MAPPING, axis=1)
    df = df.sort_values('updated_at_num', ascending=True).drop_duplicates('innCode', keep='last')

    df['name'] =  df.apply(lambda row: f"{row['lastName']} {row['firstName']} {row['fatherName']}", axis=1)
    df['innCode'] = df['innCode'].apply(fix_inn)
    return df

def preprocess_ie(df):
    df = df.rename(mapping.IE_MAPPING, axis=1)
    df['name'] =  df.apply(lambda row: f"{row['last_name']} {row['name']} {row['patronymic']}", axis=1)
    df['innCode'] = df['innCode'].apply(fix_inn)
    df['pfrNumber'] = df['pfrNumber'].apply(lambda x: None if x == 0 else x)
    df['fssCode'] = df['fssCode'].apply(lambda x: None if x == 0 else x)
    return df


def preprocess_mng(df):
    df['startDate'] = df['cdate_num'].apply(bytes_to_date)
    df['director_id'] = df['mng_ogrn'].apply(lambda x: add_id_prefix(x, 'ogrn'))
    df['organization_id'] = df['ogrn'].apply(lambda x: add_id_prefix(x, 'ogrn'))
    return df


def preprocess_org_chief(df):
    df['chief_inn'] = df['chief_inn'].apply(fix_inn)
    df['startDate'] = df['cdate_num'].apply(bytes_to_date)
    df['director_id'] = df['chief_inn'].apply(lambda x: add_id_prefix(x, 'inn'))
    df['organization_id'] = df['ogrn'].apply(lambda x: add_id_prefix(x, 'ogrn'))
    return df

def preprocess_founder(df):
    df['founder_inn'] = df['founder_inn'].apply(fix_inn)
    df['founder_ogrn'] = df['founder_ogrn'].apply(str)
    df['startDate'] = df['cdate_num'].apply(bytes_to_date)


    df['owner_id'] = df.apply(
        lambda row: add_id_prefix(row['founder_inn'], 'inn') if row['founder_ogrn'] == '0' \
                                     else add_id_prefix(row['founder_ogrn'], 'ogrn'),
    axis=1)
    df['asset_id'] = df['ogrn'].apply(lambda x: add_id_prefix(x, 'ogrn'))
    return df

def preprocess_sucession(df):
    df['date'] = df['cdate_num'].apply(bytes_to_date)
    df['predecessor_id'] = df['predecessor_ogrn'].apply(lambda x: add_id_prefix(x, 'ogrn'))
    df['sucessor_id'] = df['ogrn'].apply(lambda x: add_id_prefix(x, 'ogrn'))
    return df

def create_org(row):
    org = Organisation(row[mapping.COMPANY_MAPPING.values()])
    address = Address(row[mapping.LOCATION_MAPPING.values()])
    org.set_property('address', address.to_ftm())
    return [org.to_ftm(), address.to_ftm()]

def create_person(row):
    person = Person(row[mapping.PERSONS_MAPPING.values()])
    return [person.to_ftm()]

def create_connection(row, connType):
    connection = connType(row)
    return [connection.to_ftm()]
