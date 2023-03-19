FROM python:3.11
WORKDIR /app
RUN apt-get update && apt-get install -y dumb-init

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["dumb-init", "python", "./main.py"]