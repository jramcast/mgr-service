FROM tiangolo/meinheld-gunicorn-flask:python3.7

RUN apt-get update && \
    apt-get install -y libsndfile1 ffmpeg && \
    pip3 install pipenv

# Create app directory
RUN mkdir -p /app && mkdir /app/.tmp
WORKDIR /app

# Install app dependencies
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy

COPY . /app

EXPOSE 80
