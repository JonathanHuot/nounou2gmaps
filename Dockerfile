FROM python:2.7
WORKDIR /app

RUN pip install gunicorn futures

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ./
ENV PORT 8787
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 nounou2gmaps:app
