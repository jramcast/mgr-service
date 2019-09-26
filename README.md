# Globals service

[![pipeline status](https://git.roiback.com/core/globals-service/badges/master/pipeline.svg)](https://git.roiback.com/core/globals-service/commits/master)
[![coverage report](https://git.roiback.com/core/globals-service/badges/master/coverage.svg)](https://git.roiback.com/core/globals-service/commits/master)

Service to handle CRUD for global entities such as languages, currencies, etc.

## API

* GET /languages?locale=
* GET /languages/*code*?locale=

* GET /currencies?locale=
* GET /currencies/*code*?locale=
* GET /currencies/*code*/format/*number*?locale=

* GET /boards?locale=
* GET /board/*code*?locale=

## Development

### Make sure you have Python 3.7

You can install it with apt:

```sh
sudo apt-get update
sudo apt-get install python3.7
```

Or you can install [pyenv](https://github.com/pyenv/pyenv). A tool to easily switch between different python versions.
This tool integrates with pipenv, so that any required Python version will be automatically downloaded when running ```pipenv install```.

### Run the service locally

Install dependencies:

```sh
pipenv install --dev
```

Run

```sh
pipenv run start
```

## Deployment

Deployments are triggered when a new git tag is created.

We use git tags to semantic version the service.

To create a new version, and trigger a new deployment, use:

```sh
# Auto increments current tag with the corresponding value for releasing the next version
# Accepts a second parameter to use as commit message
./scripts/release [ major | minor | patch ] [message]
```

## Import data from bookcore

Data for globals is stored in json files in the `data` folder. You can update these files to fetch updated information from bookcore by running sync scrypts from the `sync` folder:

***NOTE**: To be able to connect to bookcore, you need to specify connection details with env variables: **BOOKCORE_PGUSER**, **BOOKCORE_PGHOST**,
**BOOKCORE_PGPASSWORD**, **BOOKCORE_PGDATABASE** and **BOOKCORE_PGPORT***

For **Boards**, run_ `pipenv run sync-boards`
