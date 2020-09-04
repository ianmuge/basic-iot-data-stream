FROM python:3.8-slim

# App setup
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install kafka-python fastapi[all] uvicorn

EXPOSE 8000
  
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000", "--reload"]