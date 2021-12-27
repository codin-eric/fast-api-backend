FROM python:3.9

RUN apt-get update

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r requirements.txt

COPY . /app/

WORKDIR /app/app

EXPOSE 8000
CMD ["uvicorn","api:app", "--host", "0.0.0.0"]