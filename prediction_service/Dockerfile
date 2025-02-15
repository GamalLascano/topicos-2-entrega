# syntax = docker/dockerfile:experimental
FROM python:3.12.7
ADD . /app
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
CMD ["python", "main.py"]