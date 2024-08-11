# Ancient Art Research Assistant 

Welcome to the Ancient Art Research Assistant project. This project runs an agent which automates one of my major hobbies: Researching historical art on the internet and blogging about it. This agent searches the web for new images of ancient artifacts to add to its collection. It then researches any new finds and produces 100 word blurbs based on the source material. It allows me to review its output periodically and then direct it to create short blog posts that references one or more of the images. 

## Live Demo

A live demo of the app can be accessed [here](https://finds-viewer-uwrcgo4b7q-ue.a.run.app/).

## Installation

### Prerequisites
An Apple machine running MacOS the M1/2 chip (not Intel).

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```
Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```

### Google Cloud Setup
This project runs on Google Cloud and assumes that you have an existing Google Cloud
account and some familiarity with Google Cloud services.

Start by installing the Google Cloud client.
```sh
brew install google-cloud-cli
```

Initialize the Google Cloud CLi tool
```sh
gcloud init
```

Create a new Google Cloud Project
```sh
GOOGLE_CLOUD_PROJECT="ancient-art-researcher"
gcloud projects create $GOOGLE_CLOUD_PROJECT --name="Ancient Art Researcher"
```

Ensure that your Project exists
```sh
gcloud projects list
```

Your project should appear in the list 
```
PROJECT_ID                  NAME                        PROJECT_NUMBER
...                         ...                         ...
ancient-art-researcher      Ancient Art Researcher      566563478993
```

Set your new project as the default 
```sh
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

Enable the Could Billing API for your project
```sh
gcloud services enable cloudbilling.googleapis.com
```

Get your billing account and link it with your project
```sh
gcloud beta billing accounts list 
gcloud beta billing projects link $GOOGLE_CLOUD_PROJECT --billing-account=[YOUR_BILLING_ACCOUNT_ID]
```

cd into the `finds_viewer` folder. This is a web app where you can view all the latest
research done by our AI researcher
```sh
cd finds_viewer
```

Enable the artifact repository API for your project
```sh
gcloud services enable artifactregistry.googleapis.com
```

### Finds Viewer Setup

Create a .env file and set the following values:
```sh
GOOGLE_CLOUD_PROJECT=ancient-art-researcher
GOOGLE_APPLICATION_CREDENTIALS=[path to JSON file with google application credentials]
BUCKET_NAME=[Google Could bucket for storing the images found by the researcher]
FIRESTORE_DATABASE=[Firestore database for saving the research]
FIRESTORE_IMAGE_COLLECTION=[Collection for storing image research findings]
REGION=[Google Cloud region for hosting the web app]
```

Create the Google storage bucket 
```sh
gcloud storage buckets create gs//$BUCKET_NAME --location=$REGION
```

Enable the Firestore API
```sh
gcloud services enable firestore.googleapis.com
```

Create the Firestore database 
```sh
gcloud firestore databases create --database=$FIRESTORE_DATABASE \
          --location=us-east1
```

Enable the Google Cloud Run API
```sh
gcloud services enable run.googleapis.com
```

Build and deploy the `finds_viewer` web application to Google Cloud
```sh
./build.sh
```

### Researcher Setup

```sh
cd ../researcher
```

Just like we did for the `finds_viewer`, create a `.env` file
```sh
OPENAI_API_KEY=[Your OpenAI API Key]
SERPER_API_KEY=[Your Serper API Key]
FIRECRAWL_API_KEY=[Your Firecrawl API Key]
GROQ_API_KEY=[Your Groq API Key]
GOOGLE_APPLICATION_CREDENTIALS=[JSON file with your Google app credentials]
GOOGLE_CLOUD_PROJECT=[Your Google cloud project name]
FIRESTORE_DATABASE=[Firestore database for saving the research]
GCLOUD_IMAGE_BUCKET=[Google Cloud Bucket for storing the images found by the researcher]
OPENAI_MODEL_NAME=gpt-4o-mini
```

You should be able to run `build.sh` to build the `researcher` docker container
```sh
./build.sh
```

To run the `researcher` locally
```sh
./run_docker.sh
```

### Deploying the Researcher to Google Cloud

#### TODO


### Ansible Setup

```bash
    brew install ansible
    ansible-galaxy collection install google.cloud

    gcloud iam service-accounts create ansible-service-account --display-name="Ansible Service Account"

    gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] --member="serviceAccount:ansible-service-account@[YOUR_PROJECT_ID].iam.gserviceaccount.com" --role="roles/compute.admin"

    gcloud iam service-accounts keys create ~/path/to/your-key-file.json --iam-account=ansible-service-account@[YOUR_PROJECT_ID].iam.gserviceaccount.com

    export GCP_AUTH_KIND=serviceaccount
    export GCP_SERVICE_ACCOUNT_FILE=~/path/to/your-key-file.json
    export GCP_PROJECT=[YOUR_PROJECT_ID]
```

#### TODO