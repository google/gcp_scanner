import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
import googleapiclient.discovery

# Load the credentials
credentials, project = google.auth.default()

# Build the service
service = googleapiclient.discovery.build('iam', 'v1', credentials=credentials)

# Get the project's service accounts
service_accounts = service.projects().serviceAccounts().list(
    name='projects/YOUR_PROJECT_ID').execute()

# Open a file to log the details
with open('dwd_sa_details.txt', 'w') as f:
    # Iterate over the service accounts
    for account in service_accounts['accounts']:
        # Get the IAM policy for the service account
        policy = service.projects().serviceAccounts().getIamPolicy(
            resource=account['name']).execute()

        # Check if the service account has the DWD role
        for binding in policy.get('bindings', []):
            if 'roles/iam.serviceAccountTokenCreator' in binding['role']:
                # Log the details into the file
                f.write(f"Service account {account['email']} has DWD permissions.\n")
