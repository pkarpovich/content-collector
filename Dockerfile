FROM python:3.11-alpine
WORKDIR /app
RUN apk add dumb-init libffi-dev alpine-sdk

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["dumb-init", "python", "./main.py"]