FROM python:3.9.6-slim-buster as prod
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*


RUN pip install poetry==1.4.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main
# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /app/src/
RUN poetry install --only main

# Install ssi_fc_data
RUN pip install /app/src/packages/ssi_fc_data-2.0.0/ssi_fc_data-2.0.0.tar.gz

CMD ["/usr/local/bin/python", "-m", "server"]

FROM prod as dev

RUN poetry install
