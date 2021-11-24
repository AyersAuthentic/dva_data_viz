# COVID-19 Remote Work

## Getting Started
- Install Conda, navigate to the directory with the `environment.yml` file, then use the command `conda env create --name envname --file=environment.yml`.
Activate this environment with `conda activate envname`

## Data Storage
[GCP Data Storage](https://console.cloud.google.com/storage/browser/additional-data)

## Dash (Data Visualization)
- Run `choropleth.py`

## Models
- Run `mental_health_clf.py`
- If you would like to retrain the model, pass in the optional command line argument `--train rf` or `--train xgb`, when you run the script
