import pandas as pd
import numpy as np
from sklearn import preprocessing

from datetime import datetime
import ast


from embeddings import word2vec_str_embedding
from data.literary_periods import literary_periods

DIR = '../data'
NAN = np.nan


def one_hot_encode_pd_column(df, col_name):
    one_hot_type = pd.get_dummies(df[col_name])
    df = df.drop(col_name, axis=1)
    df = df.join(one_hot_type)
    return df


def normalize(df):
    min_max_scaler_titles = preprocessing.MinMaxScaler()
    titles_scaled = min_max_scaler_titles.fit_transform(np.array(df).reshape(-1, 1))
    return pd.DataFrame(titles_scaled.flatten())


def str_to_year(date):
    try:
        if date[0] == '-':
            year = -int(datetime.strptime(date, '-%Y-%m-%dT%H:%M:%SZ').year)
        else:
            year = int(datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').year)
    except:
        year = np.nan
    return year


def assign_to_literary_period(date_of_birth, date_of_death):
    if isinstance(date_of_birth, str) is False or isinstance(date_of_death, str) is False:
        return np.nan

    year_of_birth = str_to_year(date_of_birth)
    year_of_death = str_to_year(date_of_death)
    if isinstance(year_of_birth, int) is False or isinstance(year_of_death, int) is False:
        return np.nan

    epoch = ''
    for period in literary_periods:
        if literary_periods[period][0] <= year_of_birth < literary_periods[period][1]:
            epoch = period
            break
    if epoch == '':
        print("no period", year_of_birth)
        exit(-1)
    return epoch


def create_str_of_influences(inf_list):
    if isinstance(inf_list, float) and np.isnan(inf_list):
        return np.nan
    else:
        return ' '.join([k[1] for k in ast.literal_eval(inf_list)])


# TODO think about missing values - they can mislead the gower distance metric
def load_and_preprocess_pg_catalog(path=f'{DIR}/pg_authors.csv', out=f'{DIR}/pg_authors_clean.csv'):
    df = pd.read_csv(path)
    df = df.fillna(NAN)
    df = df[["Type", "Title", "Language", "Subjects", "LoCC", "CreatorName",
             "DateOfBirth", "DateOfDeath", "CountryOfCitizenship", "Occupation",
             "LanguagesSpokenWrittenOrSigned", "Genre", "FieldOfWork", "MemberOf",
             "EducatedAt", "InfluencedBy"]]
    # print(df)

    df["LiteraryPeriod"] = df.apply(lambda x: assign_to_literary_period(x['DateOfBirth'], x['DateOfDeath']), axis=1)
    df.drop(['DateOfBirth', 'DateOfDeath'], axis=1, inplace=True)

    df["Title"] = df["Title"].apply(lambda x: word2vec_str_embedding(x))
    df["Title"] = normalize(df["Title"])

    df["Subjects"] = df["Subjects"].apply(lambda x: word2vec_str_embedding(x))
    df["Subjects"] = normalize(df["Subjects"])

    df["InfluencedBy"] = df.apply(lambda x: create_str_of_influences(x["InfluencedBy"]), axis=1)

    df.to_csv(out, index=False)
    return df


def load_pg_catalog_to_cluster(path=f'{DIR}/pg_catalog_to_cluster.csv'):
    df = pd.read_csv(path)
    return df


def load_preprocessed_pg_catalog(path=f'{DIR}/pg_catalog.csv'):
    df = pd.read_csv(path)
    df = df.fillna(NAN)
    return df




