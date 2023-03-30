# 📝 Installation for GCP Scanner

## Install basic dependencies

**Linux** is the preferred operating system to use while contributing to GCP Scanner. If you're using Windows, we recommend setting up [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

- Have `python` installed on your system. Check out this [link](https://www.python.org/downloads/) to download.
- have `git` installed on your system.

## Steps to follow to setup gcp-scanner

### To install the package

Install the package using `pip`

```bash
pip install https://github.com/google/gcp_scanner/archive/main.zip
```

Check if installation was done correctly -

```bash
gcp-scanner --help
```

### Build using docker

There is a docker build file if you want to run the scanner from a container: 

```bash
docker build -f Dockerfile -t sa_scanner .
```

### Build from source

1. Open the Terminal & Clone the project using

    ```bash
    git clone https://github.com/google/gcp_scanner.git
    ```

2. Then,

    ```bash
    cd gcp_scanner
    ```

3. Create a Virtual Environment to install all your dependencies with -
    - **on linux or wsl:**

    ```bash
    python3 -m venv venv
    ```

    - **on windows:**

    ```bash
    python -m venv venv
    ```

4. Activate the Virtual Environment with -
    - **on linux or wsl:**
    
    ```bash
    source venv/bin/activate
    ```

    - **on windows:**

    ```bash
    .\venv\Scripts\activate.bat
    ```

5. Install all dependencies using

    ```bash
    pip install -r requirements.txt
    ```

6. Install the tool in your local machine

    ```bash
    pip install .
    ```

7. Run to check if the tool was installed correctly

    ```bash
    gcp-scanner --help
    ```

### Some other things to keep in mind before any PR

1. Check for linting using PyLint:
    - for first time do: (to install a local copy of `pylintrc`)

    ```bash
    wget https://google.github.io/styleguide/pylintrc
    ```

    - to run `pylint` for `gcp_scanner`

    ```bash
    pylint --rcfile pylintrc --disable=W0703,R1734,R1735,C0209,C0103,R1732 src/gcp_scanner/*.py
    ```

2. Ensure that the corresponding tests are successful.

3. If any new features have been added, then check with GCP to ensure they work as expected.

### Building a standalone binary with PyInstaller

Please replace `google-api-python-client==2.80.0` with `google-api-python-client==1.8.0` in `pyproject.toml`. After that, navigate to the scanner source code directory and use pyinstaller to compile a standalone binary:

```bash
pyinstaller -F --add-data 'roots.pem:grpc/_cython/_credentials/' scanner.py
```
