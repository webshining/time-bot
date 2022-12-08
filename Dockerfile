FROM python

WORKDIR /app

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]