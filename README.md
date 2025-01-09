This is a repo for testing purposes. This repo deploys to Render using the Dockerfile. Click [here](https://github.com/irelius/python-deploy-docker) to see the repo that deploys using Docker.

## Running Locally:

If you want to see if the project is able to run locally:

1. Run `pip install -r requirement.txt` at the root of this project folder
2. Run `pipenv shell` to enter the virtual environment
3. Run `flask db upgrade && flask seed all` to prep your database
4. Run `flask run` to start the backend
5. Change directory to "/react-vite" and run `npm install`
6. Run `npm run dev` to start frontend in development

- Run `npm run build` and then `npm run preview` in the "/react-vite" to see a production level view of project
- Note: Any changes made to frontend components will require you to rerun `npm run build` before `npm run preview`. There is no `nodemon` for previewing production site

<br></br>

# Recreating Database

If you were to reset the database (delete the "migrations" and "instance" folder and recreate them), you would need to remigrate the models and reseed:

1. Assuming that you've already deleted the migrations and instance folder, run `flask db init` to create a brand new migration folder
2. In the newly created migration folder, there is a "env.py" file, open that file and...
   1. Put the following at the top of the file:
      ```
      import os
      environment = os.get.env("FLASK_ENV")
      schema_name = os.environ.get("SCHEMA")
      ```
      - This will just enable the file to access the SCHEMA value in the environment variables
   2. Then, and under the `run_migrations_online` function, edit the `context.begin_transaction` function to include:
      ```
      if environment == "production":
          connection.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
          context.execute(f"SET search_path TO {schema_name}")
      ```
      - The first command is a quality of life improvement to make sure that your schema name exists in the Postgres database
      - The second command (much more important) edits all of the tables that will be generated to be linked with the schema from your ".env" file. This prevents it from being put under the "public" schema of the Postgres database
3. Run `flask db migrate` to create the migration version file under migrations/versions
   1. At the top of the newly generated migration version file, add the following at the top the file:
      ```
      import os
      environment = os.get.env("FLASK_ENV")
      schema_name = os.environ.get("SCHEMA")
      ```
      - This allows the file to access the FLASK_ENV and SCHEMA values from your ".flaskenv" and ".env" file respectively
   - **_NOTE!!!_**: If your "FLASK_ENV" file is set to "production", your migration file will include the schema name as an option under the "create_table" functions
     - Because the schema name should be secure, you would need to make sure to abstract any instance of your schema's name with the `schema_name` variable
     - However, this is not preferred as you should be on "development" when working locally
   - Assuming that your "FLASK*ENV" file is set to "development", your migration file will \_not* have the schema name included as an additional option upon creation
     - However, these tables still need to be connected to the appropriate schema. Towards the bottom of the `upgrade` function of the migration file, add the following:
       ```
       if environment == "production":
           op.execute(f"ALTER TABLE <table name> SET SCHEMA {schema_name};")
       ```
       - This will change a table (e.g. "users") to be under the schema in your ".env" file rather than "public"
       - Note: you will need to copy and paste that line for each table generated in the migration file. So if you were creating the "users", "genres", and "songs" tables, then you'd have 3 lines where you set the schemas for each table
4. Run `flask db upgrade` this will take the migration file and run it against your database
   - If your FLASK_ENV is set to "development", sqlite
   - If your FLASK_ENV is set to "production", Postgres
     - If your local environment was set to "production", you could also use your PSQL command to see if your Postgres database correctly generated the schema and tables
       - Run `\dt <schema name>.*;` in your PSQL shell and that will list all of the tables under that schema
         - You should also see a table called "alembic_version" under this schema, that holds the alembic version number of your migration
       - You could alternatively wait until deployment to then check your Postgres database with the PSQL command
5. Run `flask seed all` to seed your database
   - If your FLASK_ENV is set to "development", sqlite
   - If your FLASK_ENV is set to "production", Postgres
     - Similarly to step 4, if your local environment was set to "production", you could check your Postgres database for the correct seed data with the PSQL command
       - Run `select * from <schema name>.<table name>;` in your PSQL shell to see the rows of that table

<br></br>

# Development vs Production Migration File

As outlined in the <a href="#recreating-database">Recreating Database</a> section, the environment directly impacts how alembic interacts with the Postgres database.

- If FLASK_ENV was set to "production", the migration file is generated with a `schema` option, set to the value of your schema name
- If FLASK_ENV was set to "development", this option and value will be missing
- There're some other differences, but they all follow that trend of "production" having the schema name and "development" not

This is important because the seeder files, upon deployment, will interact with the Postgres database assuming that the schema name exists and the tables are generated under that schema. If improperly set up, the schema name might not exist or the tables will be generated under the wrong schema (most likely "public" as that is the default schema name for Postgres).

The seeder files are currently set up to take the value from your "SCHEMA" environment variable (as indicated by your environment page on your render's webservice; for the sake of example, referred to as "test_schema"). Your seeder files will then try to input data into "test_schema".users or "test_schema".songs, but if incorrectly setup, your Postgres database might not have that. Instead, it might have "public".users and "public".songs.

There are a solutions to this issue:

1. Remove any references to "SCHEMA" in your project files so that it defaults to "public" during deployment.
   - Issue: This is not recommended. You should have a unique schema for each project and it shouldn't exist on the "public" schema. You also wouldn't be able to deploy another alembic project to this Postgres database "public" would be occupied already
   - Not best practice
2. Add "migrations" to your .dockerignore file and then add "flask db init" and "flask db migrate" to your Dockerfile so that it generates a new migration file when it's run during deployment
   - Issue: The migration version you have on deployment would be different than the one you keep locally. My instinct tells me that there are more problems to this solution, but I don't know for sure
   - Issue: You would also need to run the following in your PSQL shell before every push to main/deployment attempt: `DELETE FROM alembic_version; DROP SCHEMA <schema name> CASCADE; CREATE SCHEMA <schema name>;`
     - This could probably be resolved by editing the migrations/env.py file to run those commands at particular points
3. Change the FLASK_ENV variable in your ".flaskenv" file to "production" and change the DATABASE_URL variable in your ".env" file to the External Database URL from Render, and then run the commands to migrate, upgrade and seed in your terminal
   - A benefit to this is that you can unseed, downgrade, delete your migration folder freely. Just run `flask db init`, `flask db migrate`, `flask db upgrade`, and `flask seed all`, and it will directly change the Postgres database and alembic version
   - Issue: If you don't change FLASK_ENV back to "development" and you make changes to your database, then it will directly impact the production level database (which is not good)
4. The best solution is the one outlined under section <a href="#recreating-database">Recreating Database</a>
   - Doing it this way will allow you to keep FLASK_ENV as "development" while being able to deploy correctly
   - You could also temporarily set FLASK_ENV to "production" and set the DATABASE_URL to the external database url on your local computer to test things out, but again, this would be working directly on the Postgres database, so be careful

### Note:

- Any Foreignkeys listed in the model files for parent-child relationships will need to reference the "SCHEMA" value as well as that is how Postgres works
  - Any table is referred as: `<schema name>.<table name>`
  - Ex: If you have a table called "jazz" under the "music" schema, you'd refer to it with "music.jazz"
    - This is where the "add_prefix_for_prod" function comes in handy. It does it for you automatically. See model files for concrete example
- To reset your alembic history, enter your postgres database with your PSQL command and run one of the two followingn commands:
    1. If the alembic_version is stored under "public": `DELETE FROM alembic_version;`
    2. If the alembic_version is correctly attached to your schema name: `DELETE FROM <schema name>.alembic_version;`
    - This will clear your alembic version history and you can deploy either your Dockerfile project or directly from your repo

<br></br>

# Deployment via Dockerfile:

This project deploys to Render with the Dockerfile (not a Docker image).
Render will read the Docker file and create an image and container on their side (I assume). Ideally, you'd create a Docker image and deploy with that instead, but this pretty good as well. It gives some experience with how Dockerfiles work at least.

## Environment variables needed on **Render**:

- `DATABASE_URL`
  - Get from postgres database service. Use external database url
- `FLASK_APP`
  - Set to "app"
- `FLASK_ENV`
  - Set to "production"
- `SCHEMA`
  - Something short, concise, and descriptive of the project
  - As this is a python project, use snake_case
- `SECRET_KEY`
  - A random string of characters. Do not share. It's a secret

## Build Docker Image Locally

To build a Docker image locally, use this command template: `docker build --build-arg SCHEMA=<use your schema> --build-arg DATABASE_URL=<use the external database url of your postgres database> --build-arg SECRET_KEY=<secret key you generate> .`

- Replace the `<>` with the appropriate values

Because the Dockerfile runs flask commands to upgrade and seed your database, it must access the SCHEMA and DATABASE_URL values while building, but the values are provided by the environment variable, which is only provided by you after telling Docker to build the file (if not clear, there's an inherent issue with the order in which the steps occur)

- The command template provided above will allow you to pass in ARGs while building
- You could hard code the values directly into the Dockerfile but be careful that you don't push any sensitive info to your repo

<br>

## Dockerfile Explanation:

1. Use the python3.9.18 image
   - Could use different image, but I haven't experimented with this
2. Set work directory to `/var/www`
   - Necessary to indicate where in the Docker image will store your files
3. Copy over the requirements.txt file
   - Store the file under the name: "requirements.txt"
4. Run the command to install the packages listed under the requirements.txt file
   - psycopg2-binary was added to "requirments.txt" file, so there is no need to have a separate line in the Dockerfile to install this package
     - If you have not added this package to the requirements file, you'd need to add it separately: `RUN pip install psycopg2`
5. List variables needed

- `FLASK_APP`
  - Set to "app", hardcoding is ok
- `FLASK_ENV`
  - Set to "production", hardcoding is ok
- `SCHEMA`
  - Establish an ARG and ENV variable. Don't provide a default to ARG, but set a default variable value to the ENV (see Docker file for clarification)
- `SECRET_KEY`
  - Establish an ARG and ENV variable. Don't provide a default to ARG, but set a default variable value to the ENV (see Docker file for clarification)
- `DATABASE_URL`
  - Establish an ARG and ENV variable. Don't provide a default to ARG, but set a default variable value to the ENV (see Docker file for clarification)

6. Copy over all of the other files
   - Will not copy over "migrations" folder if it is listed in ".dockerignore" file
     - Only put "migrations" in .dockerignore file if you want to generate a new migration file upon each deployment
       - See <a href="#development-vs-production-migration-file">Development VS Production Migration File</a> for a more detailed explanation (see solution 2)

- Run `flask db upgrade` and `flask seed all` to setup and populate Postgres database
  - `flask db init` and `flask db migrate` only necessary if you want to generate a new migration file upon each deployment (again, see <a href="#development-vs-production-migration-file">Development VS Production Migration File</a> for a more detailed explanation)
- Run `gunicorn app:app` to start the app

<br></br>

## Notes:
- "psycopg2-binary" was added to requirements.txt file, version "2.9.10"
    - This means that it is not a separate package to be installed in a separate command
- Development python version is 3.9.4
- Development pip version is 24.3.1
- Development pyenv version is 2.4.20
- Ideally, create a docker image and deploy with that image rather than deploying with dockerfile on Render
    - Probably because they use the dockerfile to create their own image?
