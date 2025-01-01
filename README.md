This is a repo for testing purposes. This repo deploys to Render using the Dockerfile. Click [here](https://github.com/irelius/python-deploy-docker) to see the repo that deploys using Docker.

# Running Locally:
1. Run `pip install -r requirement.txt` at the root of this project folder
2. Run `pipenv shell` to enter the virtual environment
3. Run `flask db migrate && flask db upgrade && flask seed all` to prep your database
4. Change directory to "/react-vite" and run `npm install`
5. Run `flask run` to start the backend
6. Change directory to the "/react-vite" directory, run `npm run build` and then `npm run preview`
    - Note: Any changes made to frontend components will require you to rerun `npm run build` before `npm run preview`. There is no `nodemon` for preview 

<br></br>


# Deployment via Dockerfile:
- Environment variables needed on **Render**:
    - `DATABASE_URL`
        - Get from postgres database service. Use external database url
    - `FLASK_APP`
        - Set to "app"
    - `FLASK_ENV`
        - Set to "production"
    - `SCHEMA`
        - Something short, concise, and descriptive of the project
    - `SECRET_KEY`
        - A random string of characters. Do not share. It's a secret
    - `FLASK_DEBUG`
        - Set to true
- The Dockerfile will handle the building of the project
- To build a Docker image locally...
    - Use this command template: `docker build --build-arg SCHEMA=<use your schema> --build-arg DATABASE_URL=<use the external database url of your postgres database> --build-arg SECRET_KEY=<secret key you generate> .`
    - Because the Dockerfile runs flask commands to upgrade and seed your database, it must access the SCHEMA and DATABASE_URL values while building
        - But the values are provided by the environment variable, which is only provided by you after telling Docker to build the file (there's an order bug)
        - The command template provided above will allow you to pass in ARGs while building
    - You could hard code the values directly into the Dockerfile but be careful that you don't push any sensitive info to your repo

<br></br>

# Dockerfile:
- Needed variables on Dockerfile:
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
- Run pip install from the requirements.txt file that was copied over
- `flask db upgrade` and `flask seed all` used to populate the postgres database

<br></br>

## Notes:
- There's some issue with having multiple flask projects on one postgres database from my tests. It could be that my testing methodology is flawed, but having multiple flask projects with differing alembic identifiers seems to be causing an issue with the downgrade function
- To reset your alembic history, enter your postgres database with your PSQL command and run `DELETE FROM alembic_version;`
    - This will clear your alembic version history and you can deploy either your Dockerfile project or directly from your repo
- "psycopg2-binary" was added to requirements.txt file, version "2.9.10"
    - This means that it is not a separate package to be installed in a separate command
- Development python version is 3.9.4
- Development pip version is 24.3.1
- Development pyenv version is 2.4.20

- Ideally, create a docker image and deploy with that image rather than deploying with dockerfile on Render
    - Probably because they use the dockerfile to create their own image?
