Title: Replace in-memory store with persistent database

Description:
Migrate activities and user storage from in-memory structures to a persistent database (SQLite/Postgres) with proper migrations.

Why:
- Data survives restarts
- Enables queries, constraints, and transactions

Acceptance criteria:
- Models persisted to DB with migrations
- Existing endpoints continue to work with DB-backed models
- Update `requirements.txt` and README with DB setup instructions

Labels: database, maintenance
