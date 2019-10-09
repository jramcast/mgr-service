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


### Donwload VGGish model files

This model is necessary to convert raw audio files to AudioSet's 128-dimensional embeddings. Download these in `data/vggish`:

* [VGGish model checkpoint](https://storage.googleapis.com/audioset/vggish_model.ckpt),
  in TensorFlow checkpoint format.
* [Embedding PCA parameters](https://storage.googleapis.com/audioset/vggish_pca_params.npz),
  in NumPy compressed archive format.

More information in [VGGish model README](https://github.com/tensorflow/models/tree/master/research/audioset/vggish).


### Run the service locally

Install dependencies:

```sh
pipenv install --dev
```

Run

```sh
pipenv run serve
```
