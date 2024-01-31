ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-bullseye
LABEL maintainer="Marc Schneider"

RUN pip install poetry && poetry config virtualenvs.create false
WORKDIR /app
COPY ./config /app/config
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root --no-interaction && \
    poetry cache clear pypi --all
COPY ./src /app/src
RUN poetry install --only-root
RUN python /app/src/paraback/scraping/nltk_downloader.py

ENTRYPOINT ["/bin/bash"]
#ENTRYPOINT ["python", "-OO", "-m", "paraback", "--config", "/app/config/config.yml"]

