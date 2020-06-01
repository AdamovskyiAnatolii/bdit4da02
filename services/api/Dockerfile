# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

COPY ./requirements.txt ./

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5005

CMD ["python", "api.py"]