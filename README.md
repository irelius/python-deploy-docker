This is a repo for testing purposes. Testing deployment via Render using a Dockerfile and deployment directly from the repo.

# Starting Out:
1. Run `pip install -r requirement.txt` at the root of this project folder
2. Run `pipenv shell` to enter the virtual environment
3. Run `flask db migrate && flask db upgrade && flask seed all` to prep your database
4. Run `flask run` to start the backend
5. Change directory to "/react-vite"...
    1. Run `npm install` and `npm run build`
    2. Run `npm run dev` to run on local. To run preview of production, run `npm run preview`


# Deployment via Repo:
- Environment variables needed on Render:
    - `DATABASE_URL`
        - Get from postgres database service. Use internal database url
        - If you want to test things out on a production level without deploying to Render...
            - Change your local .env file's DATABASE_URL variable from "sqlite:///dev.db" to be the *external* database url of Render's postgres database service
            - Then change your local .env file's FLASK_ENV variable from "development" to production"
            - Then enter your shell with "pipenv shell" and migrate and seed like normal
                - Make sure that you specify the schema in your model files (refer to model files)
    - `FLASK_APP`
        - Set to "app"
    - `FLASK_ENV`
        - Set to "production"
    - `SCHEMA`
        - Something short, concise, and descriptive of the project
    - `SECRET_KEY`
        - A random string of characters. Do not share. It's a secret
- Build command: `pip install -r requirements.txt && pip install psycopg2 && flask db upgrade && flask seed undo && flask seed all`
    - Install the packages first, then unseed/downgrade so push doesn't break with unique properties on columns
    <!-- - Kinda weird that "flask db migrate" isn't included in the build command. Not really sure why it breaks when I add it ¯\\_(ツ)\_/¯ -->
- Start command: `gunicorn app:app`


# Deployment via Dockerfile:


## Notes:
- "psycopg2-binary" was added to Pipfile, version "2.9.10". Probably not needed. idk why i added it
- Development python version is 3.9.4
- Development pip version is 24.3.1
- Development pyenv version is 2.4.20



