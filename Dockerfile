FROM python:alpine

WORKDIR /app

RUN apk add --no-cache ffmpeg

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]