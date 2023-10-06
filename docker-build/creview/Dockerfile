FROM python:3.12-bookworm

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT production
ENV ALLOWED_HOSTS ${ALLOWED_HOSTS}
ENV SECRET_KEY ${SECRET_KEY}

# set work directory
WORKDIR /creview

# install dependencies
RUN pip install --upgrade pip
RUN pip install gunicorn
COPY ./requirements.txt /creview
RUN pip install --no-cache-dir --upgrade -r /creview/requirements.txt

COPY . /creview

EXPOSE 8000