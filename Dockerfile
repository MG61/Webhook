ARG PYTHON_VERSION=3.11.9
FROM python:${PYTHON_VERSION}-slim as base
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app /app

CMD ["gunicorn", "app:application", "-w", "3", "-b", "0.0.0.0:8000"]