FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y cmake libopenblas-dev liblapack-dev libjpeg-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]