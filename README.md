# Music genre classification service

WIP

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
pipenv run serve
```
