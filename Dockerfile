FROM python:3.9

ENV POETRY_VERSION=1.5.1

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /roastmate
COPY . .
RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "sanic", "roastmate.server:app", "--host=0.0.0.0"]