FROM python:3.9.18-alpine3.18

WORKDIR /var/www

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# --------------- Not necessary to run following command as it was added to requirements.txt file ---------------
# RUN pip install psycopg2 

RUN pip install --upgrade pip

# ENV for variables for future environment variables
    # Can provide a default value, but can be changed
# ARG for variables that not available after image is built
    # Running container cannot access an ARG value

ARG FLASK_APP=app
ARG FLASK_ENV=production

# Don't share secret key for security reasons
ARG SCHEMA
ENV SCHEMA=${SCHEMA}

# Don't share secret key for security reasons
ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

# Don't share secret key for security reasons
ARG DATABASE_URL
ENV DATABASE_URL=${DATABASE_URL}

COPY . . 

# # ------------- Following two steps only necessary if you add "migrations" to the .dockerignore file ------------
# # ------------------------ See "Dockerfile Deployment" section in README for explanation ------------------------
# Run flask db init
# Run flask db migrate
# # ---------------------------------------------------------------------------------------------------------------

RUN flask db upgrade
RUN flask seed all


CMD ["gunicorn", "app:app"]
# Alternatively: `CMD gunicorn app:app` should work