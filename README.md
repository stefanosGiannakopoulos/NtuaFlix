[![Backend Tests](https://github.com/ntua/softeng23-34/actions/workflows/backend_test.yml/badge.svg)](https://github.com/ntua/softeng23-34/actions/workflows/backend_test.yml)
[![Docker Compose build and up, tests for CLI client](https://github.com/ntua/softeng23-34/actions/workflows/cli_test.yml/badge.svg)](https://github.com/ntua/softeng23-34/actions/workflows/cli_test.yml)

# NTUAFLIX

## Introduction
Unlock Infinite Entertainment with NTUAFLIX: Your Gateway to Movies and Series Extravaganza! Immerse Yourself in a World of Blockbusters and Binge-Worthy Delights. Join the Streaming Revolution Now! #NTUAFLIX #Movies #Series #StreamingExcellence

Access NTUAFLIX [here](https://ntuaflix.ddnsfree.com/ "here").
<img src="/front-end/public/meta-image.png" style="border-radius:8px;"/>

## Tech Stack
<div style="display:flex; justify-content: space-between;">
<img src="https://cdn.worldvectorlogo.com/logos/fastapi.svg" width="17%"/><img src="https://www.svgrepo.com/show/354115/nginx.svg" width="17%"/><img src="https://upload.wikimedia.org/wikipedia/commons/2/29/Postgresql_elephant.svg" width="17%"/><img src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg" width="17%"/><img src="https://cdn.worldvectorlogo.com/logos/material-ui-1.svg" width="17%"/>
</div>


## Quick start (docker)

Just run:
```bash
docker compose up --build
````
The frontend will be served on port 5000 and the API on port 8000.

## Manual setup

## Prerequisites

1. [Python](https://www.python.org/downloads/) , [pip](https://pip.pypa.io/en/stable/installation/)
2. [Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
3. DBMS: [PostgreSQL](https://www.postgresql.org/download/)

## Quick Setup for Virtual Environment

### Make .venv
```bash
python3.10 -m venv .venv
```
### Activate .venv
For Windows
```bash
.venv\Scripts\activate
```
For Unix/MacOS
```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r back-end/requirements.txt
```

### Additional if you use MySQL
```bash
pip install pymysql
```

## Quick setup for frontend

```bash
npm install
```

## Local App Demo

1. Create `back-end/.env` file to configure your database credentials, check the `.env` template in `back-end/README.md`.
2. Add the following parameters for the authentication schema in the .env file you just created:
   ```
   SECRET_KEY=469155679be5db1afdb6613292c4c7805dfa71d2be7fde22d5abb522d6f23ef2
   ALGORITHM=HS256
   FORGET_PWD_SECRET_KEY=658955679be4fr3afdb6613292c4c7805dfa71d2be7fde2297abb535d6f23ef2
   ```
   
4. Create a database in your DBMS, for example `ntuaflix` and save the name in the `back-end/.env`. For the next steps your DBMS should be running (on localhost).
5. Run `back-end/models.py` to create tables of the schema.
6. Place `tsv` files for data import into a folder `back-end/truncated_data`
7. Run `back-end/input_tsv.py` to import data into the database from the tsv files.
8. Run `back-end/main.py` to run the back-end code.
9. Run `back-end/mock_data_parser.py` in a new terminal to insert mock data in the database for a full app expierence demo.
10. While `back-end/main.py` is running, open a new terminal and run `npm start` in `front-end/` folder to start the front-end.

### CLI Client

## Quickstart

To install the cli-client you can use the prebuilt wheel package (.whl) you can find in `cli-client/dist/'.
Just run:
```bash
pip install WHEEL_FILE
```

You can then immediately run the cli:
```bash
ntuaflix-cli [OPTIONS]
```

Further documentation for the cli client can be found [here](cli-client/README.md).

## Manual run

If you want to manually run the cli client enter the folder `cli-client/` and run:
```
python3 -m ntuaflix_cli [OPTIONS]
```
(you may as well use the `ntuaflix\_cli.sh [OPTIONS]` which does exactly that.

### Testing

1. To test the backend enter `backend/` and run:
```bash
pytest
```
It will create a testing instance of PostgreSQL (not just a testing db, but a whole dbms). If you want to use your own dbms instance, use the option `--use-existing-dbms yes`

Because the upload of the data is generally slow, it is not by default tested. Instead we preload a prebuilt `test.sql` file to the database. If you want to test the upload of the data, use the option `--preload no`.

2. To test the cli client ebter `cli-client/` and run:
```bash
pytest
```

The cli client testing requires a working API (this is not setup by the test, it has to be running; that's because generally the API would be served on a Server, and the cli client would be independently tested). We advise you to firstly test the API, to make sure there are no issues. If the API tests fails, with very high probability the cli client tests will also fail.


What's more, code coverage of the tests can be shown. You can add the option `--cov=.` if you want to do so.
