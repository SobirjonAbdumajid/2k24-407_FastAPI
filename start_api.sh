#!/bin/bash

uvicorn app.server.app:create_app --reload --host 0.0.0.0 --port 8000
