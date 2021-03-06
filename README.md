# Music genre classification service

This service, along with [mgr-app](https://github.com/jramcast/mgr-app) is a showcase of **Music Genre Classification** with **Audioset**, using different models.

## Citations

This application is a demo of the research conducted for the following study:

* [Machine learning for music genre: multifaceted review and experimentation with audioset](https://link.springer.com/article/10.1007/s10844-019-00582-9). 

[Read the article](https://rdcu.be/b87uq).

**If you use this code or wish to reference this work, please cite it as**:

> Ramírez, J., Flores, M.J. Machine learning for music genre: multifaceted review and experimentation with audioset. J Intell Inf Syst 55, 469–499 (2020). https://doi.org/10.1007/s10844-019-00582-9

## Related repositories

The repository for the application frontend is: https://github.com/jramcast/mgr-app

The repository for models training code is: https://github.com/jramcast/music-genre-classification-audioset

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

### Build tensorflow serving models

Tensorflow models need to be containerzied and served with **Tensorflow Serving**. To do so, you need to export tensorflow models to **Tensorflow saved model** formats:

```sh
./scripts/export_tf_serving_models
```

### Run the service locally

Install dependencies:

```sh
pipenv install --dev
```

Run

```sh
docker-compose up
```

### Prepare for production

First, make sure that Tensorflow models are exported for **Tensorflow Serving**:

```sh
./scripts/export_tf_serving_models
```

Then you can either build your Docker images and deploy them to, for example a k8s cluster, or just use docker-compose to run them.

### SSL Setup

You can follow this guide:

https://www.guyatic.net/2017/05/09/configuring-ssl-letsencrypt-certbot-nginx-reverse-proxy-nat/


## TODO

Production: Remove tmp files periodically
