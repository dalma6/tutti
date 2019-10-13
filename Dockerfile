FROM python:3.4
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD celery -A tutti.task worker --loglevel=debug
CMD python main.py