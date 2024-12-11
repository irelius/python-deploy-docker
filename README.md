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
    - Note: the ".dockerignore" file includes the "migration" folder, so the steps of initializing, migrating, and upgrading the database is necessary in the Dockerfile
        - If "migrations" is removed from the ".dockerignore" file, you can also remove the `flask db init` and `flask db migrate` commands from the Dockerfile
            - The upgrade and seeding is still necessary

<br></br>

## Notes:
- There's some issue with having multiple flask projects on one postgres database from my tests. It could be that my testing methodology is flawed, but having multiple flask projects with differing alembic identifiers seems to be causing an issue with the downgrade function
- To reset your alembic history, enter your postgres database with your PSQL command and run `DELETE FROm alembic_history;`
    - This will clear your alembic history and you can deploy either your Dockerfile project or directly from your repo
- "psycopg2-binary" was added to Pipfile, version "2.9.10". Probably not needed. idk why i added it
- Development python version is 3.9.4
- Development pip version is 24.3.1
- Development pyenv version is 2.4.20



