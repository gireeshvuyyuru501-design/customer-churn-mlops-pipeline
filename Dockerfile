FROM python:3.11-slim

WORKDIR /app

COPY requirements-docker.txt .
COPY src ./src
COPY model.joblib .

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-docker.txt

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "churn.api:app", "--host", "0.0.0.0", "--port", "8000"]