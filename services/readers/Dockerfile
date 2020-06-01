# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

COPY requirements.txt ./

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./*.py ./
COPY ./models ./models

CMD ["python", "app.py"]