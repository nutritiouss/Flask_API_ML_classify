#!/bin/bash

gunicorn -w 4 --bind=0.0.0.0:5000 --preload --reload \
          --name=regno-api --log-level info index:app
