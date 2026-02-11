FROM python:3.13.12-bookworm

WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY app ./app

CMD ["uvivorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]