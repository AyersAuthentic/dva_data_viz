from process_data import process_data

if __name__ == "__main__":
    df_master = process_data()
    df_master.to_csv('./data/master.csv')



