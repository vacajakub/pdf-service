# TODO povídaníco jsem dělal

# TODO curly 

# TODO povídání o automatickém vytvořením db

### Run in docker-compose

Run in docker compose by running `docker compose up -d --build`u

Build docker compose by `docker-compose build`, then run it by `docker-compose up -d`.

In case of changes to code, run `docker compose up -d --build`

If you want to view the logs run `docker compose logs -f`

If you want to look into the database run `docker compose exec db sh` and then `psql "host=db port=9432 user=pdf password=pdf dbname=pdf"`

Stop and remove by `docker compose down`

### Run in vscode

Dev container plugin in vscode is needed. 
Open folder in vscode, then click on open in devcontainer and you are ready to go and debug. Just launch app (or tests) through launch configuration.
