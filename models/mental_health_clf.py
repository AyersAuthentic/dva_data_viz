import pandas as pd
import numpy as np
import pickle
import argparse

from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# Parse Command Line Arguments
parser = argparse.ArgumentParser(description='COVID - Mental Health Classifier')
parser.add_argument('train', type=str)
args = parser.parse_args()


def mental_health_clf():

    # df = pd.read_csv('https://storage.googleapis.com/additional-data/cleaned_datasets/CMaster2_HPS_CDC_CPS_Vaccinated.csv')
    df = pd.read_csv('../data/CMaster2_HPS_CDC_CPS_Vaccinated.csv')
    df = df[['INCOME', 'WRKLOSS', 'MORTCONF', 'MORTLMTH', 'KINDWORK', 'CDCCOUNT', 'DOWN']]

    # Drop Missing Values and NaNs
    for col in df.columns:
        df.drop(df[df[col] == -88].index, inplace=True)
        df.drop(df[df[col] == -99].index, inplace=True)
        df.dropna(inplace=True)

    # One Hot Encode - KINDWORK
    enc_df = pd.get_dummies(df['KINDWORK'],
                            prefix='KINDWORK')
    df.drop(columns=['KINDWORK'], inplace=True)

    df = pd.concat((df, enc_df), axis=1)

    # Binarize - WRKLOSS - No=0, Yes=1
    df['WRKLOSS'] = df['WRKLOSS'].replace(to_replace=2, value=0)

    # Reorder df columns
    cols = ['INCOME',
            'WRKLOSS',
            'MORTCONF',
            'MORTLMTH',
            'CDCCOUNT',
            'KINDWORK_1',
            'KINDWORK_2',
            'KINDWORK_3',
            'KINDWORK_4',
            'KINDWORK_5',
            'DOWN']

    df = df[cols]

    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, :10],
                                                        df.iloc[:, -1],
                                                        test_size=0.20,
                                                        random_state=42)

    # If command line flag is set, train RF.
    if args.train == 'train_rf':
        print(f'Training Random Forest model...')

        # Hyperparameter Ranges for tuning
        param_grid = {'max_depth': list(range(1, 20)),
                      'n_estimators': list(range(100, 400, 50)),
                      'criterion': ['gini', 'entropy'],
                      'min_samples_split': list(range(1, 70)),
                      'min_samples_leaf': list(range(5, 50))}

        rf = RandomForestClassifier(n_jobs=-1)

        # Randomized Grid Search for Hyperparameter Tuning
        search = RandomizedSearchCV(estimator=rf, param_distributions=param_grid, cv=5, n_iter=5)

        clf = search.fit(X_train, y_train)

        # Save model to disk
        with open('mental_health_clf.pickle', 'wb') as handle:
            pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # If command line flag is set, train XGB.
    elif args.train == 'train_xgb':
        print(f'Training XGB model...')

        # Hyperparameter Ranges for tuning
        param_grid = {'max_depth': list(range(1, 20)),
                      'n_estimators': list(range(100, 400, 50)),
                      'learning_rate': np.arange(0.1, 0.9, 0.1),
                      'colsample_bytree': np.arange(0.4, 1.0, 0.1),
                      'colsample_bylevel': np.arange(0.4, 1.0, 0.1),
                      'subsample': np.arange(0.4, 1.0, 0.1)}

        xgb = XGBClassifier()

        # Randomized Grid Search for Hyperparameter Tuning
        search = RandomizedSearchCV(estimator=xgb, param_distributions=param_grid, cv=5, n_iter=5)

        clf = search.fit(X_train, y_train)

        # Save model to disk
        with open('mental_health_clf.pickle', 'wb') as handle:
            pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        with open('mental_health_clf.pickle', 'rb') as handle:
            clf = pickle.load(handle)

    print(clf.best_params_)
    print(f'Classification Accuracy (Test Set): {clf.score(X_test, y_test)}')


if __name__ == '__main__':
    mental_health_clf()
