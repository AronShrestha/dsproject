## Install Python
### Windows:
1. **Download Python:**
    - Visit the official Python website at [﻿python.org](https://www.python.org/) .
    - Navigate to the "Downloads" section.
    - Download the latest version of Python for Windows.
2. **Run the Installer:**
    - Run the downloaded installer.
    - Check the box that says "Add Python to PATH" during installation.
3. **Verify Installation:**
    - Open a command prompt and type: 
```
python3 --version
```
### Linux:
1. **Install Python:**
    - Python is often pre-installed on Linux. To install or update Python, use your package manager:
```
sudo apt update
sudo apt install python3
```
1. **Verify Installation:**
    - Open a terminal and type:
```
python3 --version
```
## Install and Activate Virtual Environment
### Windows:
1. **Open a Command Prompt:**
    - Open a command prompt or PowerShell.
2. **Install **`**virtualenv:**` 
```
pip install virtualenv
```
**Create a Virtual Environment:**

- Navigate to your project directory.
- Create a virtual environment by running:
```
python -m venv venv
```
**Activate the Virtual Environment:**

- Activate the virtual environment:
```
  .\venv\Scripts\activate
```
### Linux:
1. **Open a Terminal:**
    - Open a terminal.
2. **Install **`**virtualenv:**` 
```
sudo apt install python3-venv
```
**Create a Virtual Environment:**

- Navigate to your project directory.
- Create a virtual environment by running:
```
python3 -m venv venv
```
**Activate the Virtual Environment:**

- Activate the virtual environment:
```
source venv/bin/acivate
```
## Deactivate Virtual Environment
To deactivate the virtual environment, simply run:

### Windows and Linux:
```bash
deactivate
```
## Installing requirements
```
pip install -r requirements.txt
```



## Postgres Installation

### Windows

1. Download the PostgreSQL installer from the [official website](https://www.postgresql.org/download/windows/).
2. Run the installer and follow the on-screen instructions.
3. During installation, you'll be prompted to set a password for the default `postgres` user.

### Linux

1. Install PostgreSQL using your distribution's package manager. For example, on Ubuntu, you can run:
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### macOS

1. Install PostgreSQL using Homebrew. Run the following command in your terminal:
```
brew install postgresql
```

## Configuring database
1. After installing PostgreSQL, you can access the PostgreSQL command-line interface (CLI) using the following command:
```
psql -U postgres
```

2. Once you are in the PostgreSQL CLI, you can create and setup a  new database using the following SQL command:
```
CREATE DATABASE mydatabase;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
```

## Accessing PostgreSQL

### Windows

- You can access PostgreSQL using the pgAdmin tool, which is installed along with PostgreSQL on Windows.

### Linux and macOS

- Access PostgreSQL using the `psql` command-line tool:
```
psql -U myuser -d mydatabase -h localhost -p 5432
```


## Running the backend server
**Run the Application:**
### Webapi:

```
python console.py webapi serve
```
- This will serve the webapi on  [﻿http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [﻿http://localhost:8000/](http://localhost:8000/) .
- You should see the webapi application running.


### Salesapi:

```
python console.py salesapi serve
```
- This will serve the salesapi on  [﻿http://127.0.0.1:8002/](http://127.0.0.1:8002/) or [﻿http://localhost:8002/](http://localhost:8002/) .
- You should see the salesapi application running.


### RPC server:

```
python console.py rpc serve
```
- This will serve the rpc on  [﻿http://127.0.0.1:8003/](http://127.0.0.1:8003/) or [﻿http://localhost:8003/](http://localhost:8003/) .
- You should see the rpc application running.


### Queue worker:

```
arq webapi.webapi.worker_swarm.general_worker.WorkerSettings
```
- This will serve the redis Jobqueue for webapi