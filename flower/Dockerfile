FROM python:3.10-alpine

RUN pip install "flower==1.0.0"

EXPOSE 5555

CMD ["celery", "--broker=pyamqp://guest:guest@127.0.0.1:5672//", "flower","--broker-api=http://guest:guest@127.0.0.1:15672/api/", "--backend=redis://127.0.0.1:6379/0", "--port=5555"]