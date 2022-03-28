FROM python:3.10-slim-bullseye

COPY ["requirements.txt", "/"]

RUN pip install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* && \
    rm requirements.txt

COPY ["project-api", "/src"]
WORKDIR /src

RUN useradd -m app
USER app

EXPOSE 5000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000", "--worker", "2", "--loglevel", "info"]