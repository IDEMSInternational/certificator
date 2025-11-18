# Deploy to Google Cloud Run using Github Actions

To automatically deploy from to Cloud Run from a Github Action the following is required:

- Deployment account: a service account used to deploy the service
- Runner account: a service account under which the service will run
- Awards bucket: a storage bucket to hold rendered certificates, which will be publicly accessible
- Data bucket: a storage bucket to hold assets required by the service, such as fonts and templates
- Github Action to trigger a deployment

In outline, the Github Action will use the deployment account to create (or update) a Cloud Run service, which will run as the runner account. The two storage buckets will be mounted onto the service containers on startup. Environment variables will be set to ensure that URLs for certificates are generated correctly, referencing the awards bucket.

# Setup

## GCP

### Create runner service account

Create a new service account with no roles at the project level. When the storage buckets are created, access will be granted to this account.

### Create awards bucket

- Make the bucket [publicly readable](https://cloud.google.com/storage/docs/access-control/making-data-public)
  - In short, give the role "Storage Legacy Object Reader" to principal "allUsers"
- Create a new folder to contain the awards for each deployment
- Grant the role "Storage Object User" to the runner account to allow awards to be saved in the bucket

### Create data bucket

There is no need to make this bucket publicly accessible, so it is best to keep it private in case fonts have licensing requirements, or the certificate templates should be kept private.

Create a new folder hierarchy for each deployment, which will be mounted onto the containers in the Cloud Run service.

```
deployment_1
├── fonts
│   └── font_1.ttf
└── templates
    └── template_1.png
```

Grant the role "Storage Object Viewer" to the runner account.

### Create deployment account

Grant the following roles to this account:

- Cloud Run Admin
- Service Account User

These roles will allow this account to create Cloud Run services that run as a different service account e.g., the runner account.

Create a credentials file for this account so that Github Actions can use it to authenticate to GCP.

## Github

Create a new workflow for the deployment by saving the following content in a file under '.github/workflows' e.g. '.github/workflows/deploy\_goals\_api.yml'

```yaml
name: Deploy to Cloud Run

on:
  workflow_dispatch:

jobs:
  pipeline:
    uses: IDEMSInternational/certificator/.github/workflows/deploy.yml@1144f270b85c895727f5b025bcd411ed1ea8f3e1
    permissions:
      contents: 'read'
      id-token: 'write'
    secrets:
      credentials: ${{ secrets.GCP_CREDENTIALS }}
    with:
      image: ${{ vars.GCP_SERVICE_IMAGE }}
      region: ${{ vars.GCP_REGION }}
      service_env: ${{ vars.GCP_SERVICE_ENV }}
      service_identity: ${{ vars.GCP_SERVICE_IDENTITY }}
      service_name: ${{ vars.GCP_SERVICE_NAME }}
      bucket_name_awards: ${{ vars.GCP_BUCKET_NAME_AWARDS }}
      bucket_name_data: ${{ vars.GCP_BUCKET_NAME_DATA }}
      bucket_dir: ${{ vars.GCP_BUCKET_DIR }}
```

Create repository variables to give the deployment action the information it needs. Go to _Settings_ > _Secrets and variables_ > _Actions_; select the _Variables_ tab. Create each variable by clicking on the _New repository variable_ button. Create the following variables:

- `GCP_SERVICE_IMAGE`: container image to deploy e.g., `idems/certificator:0.3.1`
- `GCP_REGION`: Google Cloud region to deploy to e.g., `europe-west1`
- `GCP_SERVICE_ENV`: settings for the API i.e., the contents of the `.env` file, but with newlines replaced with semi-colons (;).
  - `BOX`: as usual, according to your templates
  - `FONT`: fonts will be mounted at /opt/idems/certificator/data/fonts
  - `STORAGE_ROOT`: the awards bucket will be mounted at /opt/idems/certificator/awards
  - `STATIC_URL_BASE`: should be set to the publicly accessible base URL of the awards bucket e.g., https://storage.googleapis.com/awards-bucket-name/
  - `TEMPLATES_ROOT`: templates will be mounted at /opt/idems/certificator/data/templates
- `GCP_SERVICE_IDENTITY`: email of the service account under which the API will be run - the runner account
- `GCP_SERVICE_NAME`: name of the Cloud Run service e.g., `pt-certificator-deployment-1`
- `GCP_BUCKET_NAME_AWARDS`: name of the awards bucket
- `GCP_BUCKET_NAME_DATA`: name of the data bucket
- `GCP_BUCKET_DIR`: deployment specific directory under which files will be held in each bucket

Create a repository secret to store the deployment account credentials. Go to _Settings_ > _Secrets and variables_ > _Actions_; select the _Secrets_ tab. Click on the _New repository secret_ button. Create the secret as follows:

- `GCP_CREDENTIALS`: contents of the credentials file formatted as a single line - this can be achieved with a command such as `jq -c . credentials_file.json`

# Deploy

Add fonts and templates in the appropriate place in the data bucket.

In the Github repository, navigate to _Actions_ > _Deploy to Cloud Run_ page. Click the _Run workflow_ button, then the green _Run workflow_ button.

After a successful completion, check the logs to find out what the URL of the service is.
