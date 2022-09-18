FROM python:3.10-slim 


RUN apt-get clean && apt-get update
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev build-essential gcc
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir
COPY ./ /app
CMD ["python", "./main.py"]
