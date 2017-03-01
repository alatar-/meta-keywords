#!/bin/bash
gunicorn run:app \
    --worker-class gevent \
    --bind 0.0.0.0:8000 \
    --log-file ./logs/gunicorn.log \
    --log-level DEBUG \
    --reload