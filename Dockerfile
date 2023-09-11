FROM python:3.9

ENV POETRY_VERSION=1.5.1
ENV PORT=8000

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /roastmate
COPY poetry.toml .
COPY pyproject.toml .
RUN poetry install

COPY . .

EXPOSE 8000

CMD poetry run sanic roastmate.server.app --host=0.0.0.0 --port=$PORT