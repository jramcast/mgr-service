FROM python:3.7

RUN apt-get update && \
    apt-get install -y libsndfile1 && \
    pip3 install pipenv

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Install app dependencies
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy

COPY . /app

EXPOSE 3000

CMD [ "pipenv", "run", "serve" ]
