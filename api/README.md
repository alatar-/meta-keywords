## Pre

- Python 3.5
- Install deps from `requirements.txt`
- Run tests suite: `pytest`

## Running dev

    python run.py

## Running on production

Use any production server like `gunicorn`, e.g.

    ./bin/run.sh

Note: use asycnhronous workers e.g. `gevent`-based workers.

## TODO

- cache keywords requests results to prevent reduntant queries e.g. using `redis` storage