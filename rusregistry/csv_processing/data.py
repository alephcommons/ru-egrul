import pandas as pd
import glob


def load_data_sources(path_to_folder, prefix=''):
    SOURCE_DICT = dict()

    SOURCE_DICT['companies'] = pd.concat(map(pd.read_csv, glob.glob(f'{path_to_folder}/org2{prefix}*.csv')))
    SOURCE_DICT['persons'] = pd.concat(map(pd.read_csv, glob.glob(f'{path_to_folder}/person{prefix}*.csv')))

    SOURCE_DICT['mng'] = pd.concat(map(pd.read_csv, glob.glob(f'{path_to_folder}/mng{prefix}*.csv')))
    SOURCE_DICT['founder'] = pd.concat(map(pd.read_csv, glob.glob(f'{path_to_folder}/founder{prefix}*.csv')))
    SOURCE_DICT['org_chief'] = pd.concat(map(pd.read_csv, glob.glob(f'{path_to_folder}/org_chief{prefix}*.csv')))
    SOURCE_DICT['predecessor'] = pd.concat(map(pd.read_csv, glob.glob(f'{path_to_folder}/predecessor{prefix}*.csv')))

    return SOURCE_DICT

def load_ref_tables(path_to_folder):
    REF_DICT = dict()

    REF_DICT['OPF'] = pd.read_csv(f'{path_to_folder}/opf.csv').set_index('id').to_dict()['kod']

    ref_kved = pd.read_csv(f'{path_to_folder}/okved_ref.csv')

    create_full_kved = lambda row: '.'.join([str(row['o0']), str(row['o1']), str(row['o2'])]) + ' ' + row['name']
    ref_kved['kved'] = ref_kved.apply(lambda row: create_full_kved(row), axis=1)

    REF_DICT['KVED'] = ref_kved.set_index('id').to_dict()['kved']
    REF_DICT['COUNTRY'] = pd.read_csv(f'{path_to_folder}/country.csv').set_index('id').to_dict()['name']

    return REF_DICT
