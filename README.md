# Tournament database for Swiss pairing

This project creates a Postgre SQL database for a tournament based on Swiss pairing system.
Python library psycopg2 is used to interact with the database.

# Build and run the database
From the command line, launch Postgres and execute tournament.sql script
```
psql
\i tournament.sql
```

# Run tests
```python tournament_test.py```
