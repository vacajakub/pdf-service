## PDF service

### About

Application is written with usage of FastAPI, if needed I can rewrite it to Flask (I should have more time during christmas or after, this week was really hectic, with hour there and hour of free time somewhere else),
the 2 frameworks are really similar (both lightweight). I looked and some Django tutorials and determined that since I don't (yet) know Django caveats and best practies, I would not properly demonstrate my skills with it. 
If there is a problem with this, just let me know. 

#### DB

DB schema is automatically created using mounts to docker-entrypoint. Alternatively on startup script from app could be run. Tables and schema definitions are in `/sql` folder

#### Other notes

I left comments throughout code in places that I would do differently if it should be production ready code.

- Normally I would not save image data into database, but rather use a CDN and just store url/refenrece to image inside db
- Test PDFs should be normally added to ideally by git LFS

## How to run

### Run in docker-compose

Run in docker compose by running `docker compose up -d --build`

Build docker compose by `docker compose build`, then run it by `docker compose up -d`.

In case of changes to code, run `docker compose up -d --build`

If you want to view the logs run `docker compose logs -f`

If you want to look into the database run `docker compose exec db sh` and then `psql "host=db port=9432 user=pdf password=pdf dbname=pdf"`

Stop and remove by `docker compose down`

### Run in vscode

Dev container plugin in vscode is needed. 
Open folder in vscode, then click on open in devcontainer and you are ready to go and debug. Just launch app (or unit tests) through launch configuration.


## How to call

Once app is running, interactive documentation can be found at http://localhost:8000/docs.

Alternatively you can call endpoints via curl:

Upload document:

```
curl -F "file=@{local_path_to_pdf}" --location 'http://localhost:8000/documents/'
```

Get document status:

```
curl --location 'http://localhost:8000/documents/{id}' 
```

Get normalized image:

```
curl --location 'http://localhost:8000/documents/8/pages/2' 
# add --output {filename} to save to specific file
```
