import pandas as pd


def process_data():
    '''
    Process, aggregate, join data.
    Remove missing survey values, combine into one master df and csv.
    :return:
    df
    '''
    df_hps = pd.read_csv('./data/combined_HPS_csv.csv')
    df_cdc = pd.read_csv('./data/cdc_covid_case_history_cdc_covid_agg.csv')
    df_cps = pd.read_csv('./data/cpsdatalist.csv')

    # HPS
    # Extract year and month
    df_hps['year'] = df_hps['WEEK'].str[:4]
    df_hps['month'] = df_hps['WEEK'].str[5:8]
    df_hps['month'] = pd.to_datetime(df_hps['month'], format='%b')
    df_hps['month'] = df_hps['month'].dt.month

    # Drop Missing Values and NaNs
    for col in df_hps.columns:
        df_hps.drop(df_hps[df_hps[col] == -88].index, inplace=True)
        df_hps.drop(df_hps[df_hps[col] == -99].index, inplace=True)
        df_hps.dropna(inplace=True)

    # Rename State Fips to 'GESTFIPS'
    df_hps.rename(columns={"EST_ST": "GESTFIPS"}, inplace=True)

    # Drop unnecessary columns
    df_hps.drop(columns=['WEEK', 'EST_MSA'], inplace=True)

    # Downcast to smaller data types (reduced memory consumption)
    df_hps = df_hps.apply(pd.to_numeric, downcast='unsigned')

    # CDC
    # Extract year and month
    df_cdc['year'] = df_cdc['case_month'].str[:4]
    df_cdc['year'] = pd.to_numeric(df_cdc['year'], downcast='unsigned')
    df_cdc['month'] = df_cdc['case_month'].str[5:8]
    df_cdc['month'] = pd.to_numeric(df_cdc['month'], downcast='unsigned')

    # Drop NaNs
    df_cdc.dropna(inplace=True)

    # Convert State to FIPS code
    df_cdc['GESTFIPS'] = df_cdc['res_state'].apply(get_fips)

    # Drop unnecessary columns
    df_cdc.drop(columns=['res_state', 'res_county', 'county_fips', 'case_month'], inplace=True)

    # Aggregate by state, month, year
    df_cdc = df_cdc.groupby(['GESTFIPS', 'year', 'month']).sum()

    # Downcast to smaller data types (reduced memory consumption)
    df_cdc = df_cdc.apply(pd.to_numeric, downcast='unsigned')

    # CPS
    df_cps.rename(columns={'HRYEAR4': 'year', 'HRMONTH': 'month'}, inplace=True)

    # Downcast to smaller data types (reduced memory consumption)
    df_cps = df_cps.apply(pd.to_numeric, downcast='unsigned')

    # Read in with chunks due to memory constraints
    df_master = pd.merge(df_cdc, df_cps, how='inner', on=['GESTFIPS', 'year', 'month'])

    print(f'df_master: {df_master.head}')
    return df_master


def get_fips(state):
    state_dict = {
        'AL': 1,
        'AK': 2,
        'AZ': 4,
        'AR': 5,
        'CA': 6,
        'CO': 8,
        'CT': 9,
        'DE': 10,
        'DC': 11,
        'FL': 12,
        'GA': 13,
        'HI': 15,
        'ID': 16,
        'IL': 17,
        'IN': 18,
        'IA': 19,
        'KS': 20,
        'KY': 21,
        'LA': 22,
        'ME': 23,
        'MD': 24,
        'MA': 25,
        'MI': 26,
        'MN': 27,
        'MS': 28,
        'MO': 29,
        'MT': 30,
        'NE': 31,
        'NV': 32,
        'NH': 33,
        'NJ': 34,
        'NM': 35,
        'NY': 36,
        'NC': 37,
        'ND': 38,
        'OH': 39,
        'OK': 40,
        'OR': 41,
        'PA': 42,
        'RI': 44,
        'SC': 45,
        'SD': 46,
        'TN': 47,
        'TX': 48,
        'UT': 49,
        'VT': 50,
        'VA': 51,
        'WA': 53,
        'WV': 54,
        'WI': 55,
        'WY': 56,
        'AS': 60,
        'GU': 66,
        'MP': 69,
        'PR': 72,
        'VI': 78
    }

    return state_dict[state]
