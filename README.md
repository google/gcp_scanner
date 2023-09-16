![pytests](https://github.com/google/gcp_scanner/actions/workflows/python-app.yml/badge.svg)
[![GCP scanner version](https://img.shields.io/github/v/release/google/gcp_scanner?label=version&color=blue)](https://github.com/google/gcp_scanner/releases/latest)

### Disclaimer

This project is not an official Google project. It is not supported by
Google and Google specifically disclaims all warranties as to its quality,
merchantability, or fitness for a particular purpose.

### GCP Scanner

![Logo](misc/gcp_scanner_logo.png?raw=true "Logo of GCP Scanner")

This is a GCP resource scanner that can help determine what level of access certain credentials possess on GCP. The scanner is designed to help security engineers evaluate the impact of a certain VM/container compromise, GCP service account or OAuth2 token key leak.

Currently, the scanner supports the following GCP resources:

- GCE
- GCS
- GKE
- App Engine
- Cloud SQL
- BigQuery
- Spanner
- Pub/Sub
- Cloud Functions
- BigTable
- CloudStore
- KMS
- Cloud Services
- The scanner supports SA [impersonation](https://cloud.google.com/iam/docs/impersonating-service-accounts)

The scanner supports extracting and using the following types of credentials:

- GCP VM instance metadata;
- User credentials stored in gcloud profiles;
- OAuth2 Refresh Token with cloud-platform scope granted;
- GCP service account key in JSON format.

The scanner does not rely on any third-party tool (e.g. gcloud). Thus, it can be compiled as a standalone tool and used on a machine with no GCP SDK installed (e.g. a Kubernetes pod). However, please keep in mind that the only OS that is currently supported is Linux.

Please note that GCP offers [Policy Analyzer](https://cloud.google.com/policy-intelligence/docs/analyze-iam-policies) to find out which principals (users, service accounts, groups, and domains), have what access to which Google Cloud resources. However, it requires specific permissions on the GCP project and the Cloud Assets API needs to be enabled. If you just have a GCP SA key, access to a previously compromised VM, or an OAUth2 refresh token, gcp_scanner is the best option to use.

### Installation

To install the package, use `pip` (you must also have `git` installed):

```
pip install gcp_scanner
python3 -m gcp_scanner --help
```

Alternatively:

```
git clone https://github.com/google/gcp_scanner
cd gcp_scanner
pip install .
gcp-scanner --help
```

There is a docker build file if you want to run the scanner from a container:
`docker build -f Dockerfile -t sa_scanner .`

### Command-line options

```
usage: python3 scanner.py -o folder_to_save_results -g -

GCP Scanner

options:
  -h, --help            show this help message and exit
  -ls, --light-scan     Return only the most important GCP resource fields in the output.
  -k KEY_PATH, --sa-key-path KEY_PATH
                        Path to directory with SA keys in json format
  -g GCLOUD_PROFILE_PATH, --gcloud-profile-path GCLOUD_PROFILE_PATH
                        Path to directory with gcloud profile. Specify - to search for credentials in default gcloud config path
  -m, --use-metadata    Extract credentials from GCE instance metadata
  -at ACCESS_TOKEN_FILES, --access-token-files ACCESS_TOKEN_FILES
                        A list of comma separated files with access token and OAuth scopes.TTL limited. A token and scopes should be stored in JSON format.
  -rt REFRESH_TOKEN_FILES, --refresh-token-files REFRESH_TOKEN_FILES
                        A list of comma separated files with refresh_token, client_id,token_uri and client_secret stored in JSON format.
  -s KEY_NAME, --service-account KEY_NAME
                        Name of individual SA to scan
  -p TARGET_PROJECT, --project TARGET_PROJECT
                        Name of individual project to scan
  -f FORCE_PROJECTS, --force-projects FORCE_PROJECTS
                        Comma separated list of project names to include in the scan
  -c CONFIG_PATH, --config CONFIG_PATH
                        A path to config file with a set of specific resources to scan.
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set logging level (INFO, WARNING, ERROR)
  -lf LOG_FILE, --log-file LOG_FILE
                        Save logs to the path specified rather than displaying in console
  -pwc PROJECT_WORKER_COUNT, --project-worker-count PROJECT_WORKER_COUNT
                        Set limit for project crawlers run in parallel.
  -rwc RESOURCE_WORKER_COUNT, --resource-worker-count RESOURCE_WORKER_COUNT
                        Set limit for resource crawlers run in parallel.

Required parameters:
  -o OUTPUT, --output-dir OUTPUT
                        Path to output directory
```

Option `-f` requires an additional explanation. In some cases, the service account does not have permissions to explicitly list project names. However, it still might have access to underlying resources if we provide the correct project name. This option is specifically designed to handle such cases.

### Building a standalone binary with PyInstaller

Please replace `google-api-python-client==2.80.0` with `google-api-python-client==1.8.0` in `pyproject.toml`. After that, navigate to the scanner source code directory and use pyinstaller to compile a standalone binary:

`pyinstaller -F --add-data 'roots.pem:grpc/_cython/_credentials/' scanner.py`

### Working with results

The GCP Scanner produces a standard JSON file that can be handled by any JSON Viewer or DB. We are providing a web-based tool that can help you visualize the results.
To run the tool, please use the following command:

```
usage: gcp-scanner-visualizer -p 8080

GCP Scanner Visualizer

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to listen on default 8080
```

To know more about how to use the tool, please visit [GCP Scanner Visualizer Usage Guide](./visualization_tool/USAGE.md) page.

If you just need a convenient way to grep JSON results, we can recommend [gron](https://github.com/tomnomnom/gron).

### Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details.

### License

Apache 2.0; see [`LICENSE`](LICENSE) for details.
