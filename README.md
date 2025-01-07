This is a repo for testing purposes. This repo deploys to Render using the Dockerfile. Click [here](https://github.com/irelius/python-deploy-docker) to see the repo that deploys using Docker.

## <b>IMPORTANT TO NOTE</b>: <br></br> "FLASK_ENV" in the .flaskenv file is set to "production". This choice is explained later under the <a href="#dockerfile-deployment">"Deployment via Dockerfile"</a> section

<br></br>

## Running Locally:
1. Run `pip install -r requirement.txt` at the root of this project folder
2. Run `pipenv shell` to enter the virtual environment
3. Run `flask db upgrade && flask seed all` to prep your database
4. Run `flask run` to start the backend
5. Change directory to "/react-vite" and run `npm install`
6. Run `npm run dev` to start frontend in development
- Run `npm run build` and then `npm run preview` in the "/react-vite" to see a production level view of project
   - Note: Any changes made to frontend components will require you to rerun `npm run build` before `npm run preview`. There is no `nodemon` for previewing production site


<br></br>

## Deployment via Dockerfile:
### Environment variables needed on **Render**:
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
    
### Dockerfile Deployment
- When you run `flask db migrate` you create a migration file. This is created on your local computer (which is probably has FLASK_ENV set to "development")
- When you push your project, you're pushing up the migration file that was created under the "development" environment
    - This migration file will be missing the "schema" option, explanation in the next few bullet points
- Render takes that push and gets your Dockerfile, reads it, and creates their image/container to deploy
- When they're reading/executing your Dockerfile, the environment has now switched to "production" (as indicated by your environment page on your render's webservice)
- This is an issue because your migration file (that was generated under "development") will be missing the schema option
    - The conditional in each model file where you run `__table_args__ = {'schema': SCHEMA}` is what determines this (i think)
    - Under sqlite3, this is no problem, but it is a problem under Postgres (which requires a schema name) because any table that is not associated with a schema name is defaulted to the "public" schema
- Your model and seeder files will take the value from your "SCHEMA" environment variable (as indicated by your environment page on your render's webservice; for the sake of example, call it "test_schema")
- So your seeder files will try to input data into "test_schema".users or "test_schema".songs, but your Postgres database doesn't have that. It has "public".users and "public".songs
- A few ways to fix this:
    1. Solution 1 - Remove any references to "SCHEMA" in your project files so that it defaults to "public" during deployment
        - Issue: This is not recommended. You should have a unique schema for each project and it shouldn't exist on the "public" schema. Not best practice
    2. Solution 2 - Add "migrations" to your .dockerignore file and then add "flask db init" and "flask db migrate" to your Dockerfile so that it generates a new migration file when it's run during deployment
        - Issue: The migration version you have on deployment would be different than the one you keep locally. My instinct tells me that there are more problems to this solution, but I don't know for sure
        - Issue: You would also need to run the following in your PSQL shell before every push to main/deployment attempt: `DELETE FROM alembic_version; DROP SCHEMA <schema name> CASCADE; CREATE SCHEMA <schema name>;`
    3. Solution 3 - Change the "FLASK_ENV" variable in your .flaskenv file to "production" and change the "DATABASE_URL" variable in your .env file to the External Database URL from Render, and then run the commands to migrate, upgrade and seed in your terminal
        - Another benefit is that you can unseed, downgrade, delete your migration folder, run `flask db init`, `flask db migrate`, `flask db upgrade`, and `flask seed all`, and it will directly change the Postgres database and alembic version
        - Issue: You would need to change between "development" and "production" and change your DATABASE_URL between "sqlite:///dev.db" and the external database url anytime you needed to change the migration version file
            - If you don't change to "development" and you make changes to your database, then it will directly impact the production level database (which is not good)
- Method 2 or 3 is your best bet (method 3 kinda seems like the easiest?)
- Note 1: While creating the migration file under the "production" environment fixes where the model/seeder files will look at during deployment, your migration version number will still be stored under the "public" schema
    - To update this and store it under your schema name...
        1. Go to your migraionts/env.py file (after you created the migration file)
        2. Add the following two lines to the top of the file:
            ```
            import os
            schema_name = os.environ.get('SCHEMA')
            ```
        3. Scroll down to the `run_migrations_online` function and edit the `context.configure` function to include the following:
            ```
            version_table="alembic_version",
            version_table_schema=schema_name
            ```
            - See the migrations/env.py file to see a more concrete example
    - This does mean that you'd need to add those lines if you were to delete your migration file and recreate it for whatever reason
- Note 2: The schema needs to exist in the Postgres database before you try to deploy (maybe a way to customize the Dockerfile to do this?), and if your migration file's alembic version is different from what is kept in your Postgres databases's alembic_version, it would cause an error (again, maybe a way to clear the alembic_version in the Dockerfile?)
    - If you've taken the steps to store the alembic_version number under the schema name rather than "public", then you can just run `DROP SCHEMA <schema name> CASCADE; CREATE SCHEMA <schema name>;`
    - If the alembic version number is generated under "public", use the PSQL command and run `DELETE FROM alembic_version; DROP SCHEMA <schema name> CASCADE; CREATE SCHEMA <schema name>;` to reset both the alembic_version and schema

### Note:
- Any Foreignkeys listed in the model files for parent-child relationships will need to reference the "SCHEMA" value as well as that is how Postgres works
    - Any table is referred as: `<schema name>.<table name>`
    - Ex: If you have a table called "jazz" under the "music" schema, you'd refer to it with "music.jazz"
        - This is where the "add_prefix_for_prod" function comes in handy. It does it for you automatically. See model files for concrete example

### Dockerfile Local
- To build a Docker image locally...
    - Use this command template: `docker build --build-arg SCHEMA=<use your schema> --build-arg DATABASE_URL=<use the external database url of your postgres database> --build-arg SECRET_KEY=<secret key you generate> .`
        - Fill in the values in the `<>`
    - Because the Dockerfile runs flask commands to upgrade and seed your database, it must access the SCHEMA and DATABASE_URL values while building
        - But the values are provided by the environment variable, which is only provided by you after telling Docker to build the file (if not clear, there's an inherent issue with the order in which the steps occur)
        - The command template provided above will allow you to pass in ARGs while building
    - You could hard code the values directly into the Dockerfile but be careful that you don't push any sensitive info to your repo

<br></br>

## Dockerfile Explanation:
1. Use the python3.9.18 image
    - Could use different image, but I haven't experimented with this
2. Set work directory to `/var/www`
    - Necessary to indicate where in the Docker image will store your files
3. Copy over the requirements.txt file
    - Store the file under the name: "requirements.txt"
4. Run the command to install the packages listed under the requirements.txt file
    - psycopg2 was added to requirments.txt file, so not need to have separate command to install
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
- Copy over all of the other files
    - Will not copy over "migrations" folder if listed in .dockerignore file
        - Only put "migrations" in .dockerignore file if you want to generate a new migration file upon each deployment
            - See <a href="#dockerfile-deployment">"Deployment via Dockerfile"</a> for more explanation
- Run `flask db upgrade` and `flask seed all` to setup and populate Postgres database
    - `flask db init` and `flask db migrate` only necessary if you want to generate a new migration file upon each deployment
- Run `gunicorn app:app` to start the app

<br></br>

### Notes:
- To reset your alembic history, enter your postgres database with your PSQL command and run `DELETE FROM alembic_version;`
  - This will clear your alembic version history and you can deploy either your Dockerfile project or directly from your repo
  - If you've edited your migraionts/env.py file to specify the schema name for your alembic_version table, then run `DELETE FROM <your schema name>.alembic_version;`
- "psycopg2-binary" was added to requirements.txt file, version "2.9.10"
  - This means that it is not a separate package to be installed in a separate command
- Development python version is 3.9.4
- Development pip version is 24.3.1
- Development pyenv version is 2.4.20

- Ideally, create a docker image and deploy with that image rather than deploying with dockerfile on Render
  - Probably because they use the dockerfile to create their own image?
