FROM python:3.10-slim-bullseye

COPY ["requirements.txt", "/"]

RUN pip install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* && \
    rm requirements.txt

COPY ["project-worker", "/src"]
WORKDIR /src

RUN useradd -m app
USER app

CMD ["celery", "-A", "tasks:app", "worker", "--pool", "prefork", "-Q", "project-worker", "--concurrency=2", "-n", "worker@%h"]