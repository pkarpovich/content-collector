FROM python:3.11-alpine
WORKDIR /app
RUN apk update && apk add dumb-init libffi-dev alpine-sdk

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

COPY . .

CMD ["dumb-init", "python", "./main.py"]