# 📝 Installation for GCP Scanner

## Install basic dependencies

**Linux** is the preferred operating system to use while contributing to GCP Scanner. If you're using Windows, we recommend setting up [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

- Have `python` installed on your system. Check out this [link](https://www.python.org/downloads/) to download.
- have `git` installed on your system.

## Steps to follow to setup gcp-scanner

### To install the package

Install the package using `pip`

```bash
pip install gcp-scanner
```

Check if installation was done correctly

```bash
gcp-scanner --help
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

3. Create a Virtual Environment to install all your dependencies with

   - **on linux or wsl:**

   ```bash
   python3 -m venv venv
   ```

   - **on windows:**

   ```bash
   python -m venv venv
   ```

   - **on MacOS:**

   ```zsh
   python3 -m venv venv
   ```

4. Activate the Virtual Environment with

   - **on linux or wsl:**

   ```bash
   source venv/bin/activate
   ```

   - **on windows:**

   ```bash
   .\venv\Scripts\activate.bat
   ```

   - **on MacOS:**

   ```zsh
   source venv/bin/activate
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

### Build using docker

There is a docker build file if you want to run the scanner from a container:

```bash
docker build -f Dockerfile -t sa_scanner .
```
