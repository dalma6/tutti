# Tutti Crawler

Python craweler for getting info about sold items on tutti.ch

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

What things you need to install the software and how to install them

```
python3.4
```

### Installing

Install requirements

```
pip install -r requirements.txt
```

Run celery worker

```
celery -A tutti.task worker --loglevel=debug
```

Run tasks
```
python main.py
```

## Built With

* python3.4
* Grab - The scraping framework used
* celery - The task queue implementation used

## Docker

* Dockerfile is implemented but not properly working.

## Known bugs

* BacklogLimitExceeded for > 1000 celery tasks in queue

## Authors

* **Dalma Beara** - [github](https://github.com/dalma6)
