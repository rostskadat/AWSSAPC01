#!/bin/sh

sam build && \
    sam local invoke --event events/event.json {{ cookiecutter.project_name }}Function