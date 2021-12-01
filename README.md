# COVID-19 Remote Work

## Getting Started
- Install Conda, navigate to the directory with the `environment.yml` file, then use the command `conda env create --name envname --file=environment.yml`.
Activate this environment with `conda activate envname`

## Data Storage
[GCP Data Storage](https://console.cloud.google.com/storage/browser/additional-data)

- Data for all microserves is uploaded and retrieved from a Google Cloud Storage bucket.

## Dash (Data Visualization)
- Interactive Data Visualization micro services that analyze important trends related to the Covid-19 pandemic.

Each visualization application was developed using the Dash Plotly python framework. Dash is a python framework that facilitates the rapid development and deployment of interactive data visualization applications. Each application is deployed to the Google Cloud Service platform as a serverless microservice that can be easily incorporated into any front-end application using a link placed into an iframe html element. 

## Dash Requirements
- dash
- dash-bootstrap-components
- dash-core-components
- dash-html-components
- dash-table
- flask
- numpy
- pandas
- pandas-datareader
- plotly

## Run Local Demo

- Scatter Mapbox Application

```console
cd SCATTER_APP
python app.py
```

- Time Series Analysis Application

```console
cd TIME_APP
python app.py
```

- Correlation Analysis Application

```console
cd HEAT_APP
python app.py
```

- Covid Trends Analysis Application

```console
cd TREND_APP
python app.py
```

- Covid Mental Health Predictin Application

```console
cd PRED_APP
python app.py
```

## Deploy Microservce Applications to Google Cloud
- Deployment to the Google Cloud run serverless cloud is facilitated by a Docker container image from within each microservice application file. To submit and deploy each microservice application create a new google cloud project and install the google cloud SDK on your local machine. Once the SDK is installed, enter the application directory and run the console commands below:

- GCC SDK installation instructions:  https://cloud.google.com/sdk/docs/install


```console
cd (SERVICE)_APP 
gcloud builds submit --tag gcr.io/(GCC-PROJECT-NAME-ID)/app  --project=GCC-PROJECT-NAME-ID 

gcloud run deploy --image gcr.io/(GCC-PROJECT-NAME-ID)/app --platform managed  --project=(GCC-PROJECT-NAME-ID) --allow-unauthenticated

```



## Models
- Run `mental_health_clf.py`
- If you would like to retrain the model, pass in the optional command line argument `--train rf` or `--train xgb`, when you run the script
