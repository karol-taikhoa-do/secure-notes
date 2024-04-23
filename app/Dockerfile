FROM python:3.11.3-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip 
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


COPY . /app/
RUN pip install python-dotenv

CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.app:app"]
