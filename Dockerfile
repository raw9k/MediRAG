FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

# Install CPU-only PyTorch
RUN pip install --no-cache-dir \
    "torch==2.14.0+cpu" \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY vectorstore ./vectorstore

EXPOSE 10000

CMD ["sh", "-c", "uvicorn app.api.main:app --host 0.0.0.0 --port ${PORT:-10000}"]