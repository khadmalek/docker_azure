#!/bin/bash

python3 populate_db_sqlserver.py

uvicorn main:app --reload --host 0.0.0.0 --port 8000