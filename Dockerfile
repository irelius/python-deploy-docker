# template uses alpine3.18, but trying out slim-bookworm with python version 3.12
# theoretically, there shouldn't be an error between 3.9 and 3.12, but possible. we'll see
# FROM python:3.12-slim-bookworm
FROM python:3.9.18-alpine3.18

WORKDIR /var/www

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

# ENV for variables for future environment variables
    # Can provide a default value, but can be changed
# ARG for variables that not available after image is built
    # Running container cannot access an ARG value    
ARG FLASK_APP=app
ARG FLASK_ENV=production

ARG SCHEMA
ENV SCHEMA=${SCHEMA}

ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

ARG DATABASE_URL
ENV DATABASE_URL=${DATABASE_URL}

COPY . .

RUN flask db upgrade
RUN flask seed all


CMD ["gunicorn", "app:app"]