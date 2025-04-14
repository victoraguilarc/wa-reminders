FROM python:3.12-slim AS image_base

ENV NODE_VERSION 18.17.0
ENV POETRY_VERSION=1.8.4 \
    POETRY_VIRTUALENVS_CREATE=false

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONDEBUG 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential libssl-dev libffi-dev \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext bash xz-utils curl nodejs npm \
  # Timezone
  && apt-get install -y tzdata \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ENV TZ UTC

RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml /app/

RUN poetry config --local installer.no-binary psycopg2
RUN poetry install --no-interaction --no-ansi --with dev

COPY docker/post-build /post-build
RUN sed -i 's/\r//' /post-build
RUN chmod +x /post-build

ENV CHAMBER_VERSION=3.1.1
RUN curl -sSL https://github.com/segmentio/chamber/releases/download/v${CHAMBER_VERSION}/chamber-v${CHAMBER_VERSION}-linux-amd64 > /chamber \
    && chmod +x /chamber

EXPOSE 8000

#
#  P R O D U C T I O N
#
FROM image_base AS production

COPY docker/start-prod /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY docker/start-worker /start-worker
RUN sed -i 's/\r//' /start-worker
RUN chmod +x /start-worker


COPY . /app
CMD ["/start"]


#
#  D E V E L O P M E N T
#
FROM image_base AS development

COPY docker/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY docker/start-dev /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

ENTRYPOINT ["/entrypoint"]
CMD ["/start"]

