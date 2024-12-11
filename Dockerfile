# template uses alpine3.18, but trying out slim-bookworm with python version 3.12
# theoretically, there shouldn't be an error between 3.9 and 3.12, but possible. we'll see
# FROM python:3.12-slim-bookworm

FROM python:3.9.18-alpine3.18

# ENV FLASK_APP=${FLASK_APP}
# ENV FLASK_DEBUG=${FLASK_DEBUG}
# ENV FLASK_RUN_PORT=${FLASK_RUN_PORT}
# ENV FLASK_ENV=${FLASK_ENV}

# ENV SECRET_KEY=${SECRET_KEY}
# ENV SCHEMA=${SCHEMA}
# ENV DATABASE_URL=${DATABASE_URL}

ENV FLASK_APP=app
ENV FLASK_DEBUG=true
ENV FLASK_ENV=production

ENV SECRET_KEY=soierfghsoierhg6843684
ENV SCHEMA=python_deploy_docker
ENV DATABASE_URL=postgresql://irelius_database_woof_user:C2ZQQzvUBIZzBugfEMTPNtgBpEkKkn7u@dpg-ctcdd0rtq21c73foic80-a.oregon-postgres.render.com/irelius_database_woof

WORKDIR /var/www

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary
RUN pip install --upgrade pip

COPY . .

RUN flask db init
RUN flask db migrate -m 'first docker migration'
RUN flask db upgrade
RUN flask seed all


CMD ["gunicorn", "app:app"]