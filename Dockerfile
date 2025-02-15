
# pull the official docker image
FROM python:3.11.11-alpine

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY ./requirements.txt ./requirements.txt

# install dependencies
RUN pip install -r requirements.txt 

# copy project
COPY . .

# set work directory
WORKDIR /app