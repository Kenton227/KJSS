# Local Development & Testing
To run your server locally:

**1. Install Dependencies**

* Run ```uv sync``` in terminal

**2. Set Up Docker**

* Run the following command in terminal:
    ~~~
    docker run --name mypg -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb -p 5433:5433 -d postgres:latest
    ~~~
* In the future, you can start the container by just running: ```docker start mypg```

**3. Upgrade Database to Latest Schema**

* Upgrade the database to your latest schema
    ~~~
    uv run alembic upgrade head
    ~~~

**4. Create New Connection**

* Install DBeaver if you haven't
* Create a new connection in DBeaver using the connection string: ```postgresql://myuser:mypassword@localhost:5433/mydb```


SUPABASE PW: Dmdv0v7r2DTSHHHW
CONNECTION STRING: ```postgresql+psycopg://postgres.cebjtmgzkzrzhwsedyiu:Dmdv0v7r2DTSHHHW@aws-0-us-west-1.pooler.supabase.com:5432/postgres```
