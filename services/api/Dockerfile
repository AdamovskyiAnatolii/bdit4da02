# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /home/vlad/PycharmProjects/bdit4da2/services/api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5005
ENTRYPOINT ["python"]
CMD ["api.py"]