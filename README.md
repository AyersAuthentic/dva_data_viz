# COVID-19 Remote Work

## Data Storage
[GCP Data Storage](https://console.cloud.google.com/storage/browser/additional-data)

- Data for all microservices is uploaded and retrieved from a Google Cloud Storage bucket.

## Dash (Data Visualization)
- Interactive Data Visualization micro services that analyze important trends related to the Covid-19 pandemic.

Each visualization application was developed using the Dash Plotly python framework. Dash is a python framework that facilitates the rapid development and deployment of interactive data visualization applications. Each application is deployed to the Google Cloud Service platform as a serverless microservice that can be easily incorporated into any front-end application using a link placed into an iframe html element. 

## Requirements
### Dash Requirements
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

### ML Modeling Requirements
- Install Conda
- Navigate to the directory with the `environment.yml` file 
- Create the Conda environment from the environment.yml file with `conda env create --name envname --file=environment.yml`
- Activate this environment with `conda activate envname`

### Jupyter Notebook Requirements
- Install Conda or another Jupyter-enabled environment, using *ML Modeling Requirements* above.
- Open any of the *.ipynb* files found within the /models folder.
- Execute Notebook code. For any additional libraries, if using a Conda environment, use the cmdline to execute `pip install [package name]`. Otherwise, ensure your Python environment has the necessary libraries installed.

### Website Requirements
- A local copy of the website can be found in the folder *website/startbootstrap-resume-gh-pages*. To run, clone this repository to your local computer and open the `index.html` found within in the browser of your choice (it's recommended to use a modern browser, such as Google Chrome, Mozilla Firefox or Microsoft Edge. Internet Explorer or other browsers may have compatibility issues).
- Dash Apps are deployed to the website and will run even if opened locally.


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

- Covid Mental Health Prediction Application

```console
cd PRED_APP
python app.py
```

## Deploy Microservice Applications to Google Cloud
- Deployment to the Google Cloud run serverless cloud is facilitated by a Docker container image from within each microservice application file. To submit and deploy each microservice application create a new google cloud project and install the google cloud SDK on your local machine. Once the SDK is installed, enter the application directory and run the console commands below:

- GCC SDK installation instructions:  https://cloud.google.com/sdk/docs/install


```console
cd (SERVICE)_APP 
gcloud builds submit --tag gcr.io/(GCC-PROJECT-NAME-ID)/app  --project=GCC-PROJECT-NAME-ID 

gcloud run deploy --image gcr.io/(GCC-PROJECT-NAME-ID)/app --platform managed  --project=(GCC-PROJECT-NAME-ID) --allow-unauthenticated

```

## Machine Learning Models
- Run `mental_health_clf.py` to run the classification model, and view its Test Set Accuracy
- Run `mental_health_rgr.py` to run the regression model, and view its Test Set Accuracy
- To retrain the model, pass in the optional command line argument `--train rf` (Random Forest Model) or `--train xgb` (XGBoost Model), when you run the script
