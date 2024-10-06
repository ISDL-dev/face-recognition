FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y cmake libopenblas-dev liblapack-dev libjpeg-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]