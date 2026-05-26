Title: Add Django + DRF backend option

Description:
Add an optional Django + Django REST Framework backend to support persistent models, admin UI and richer REST APIs. This is an architectural spike to evaluate migrating from the current in-memory FastAPI implementation to a database-backed Django project or adding a Django microservice.

Why:
- Persistent storage for activities and users
- Leverage Django admin for club management
- Easier role-based access and model validations

Acceptance criteria:
- Spike repo or scaffold added under `django/` or `services/django-backend`
- README addition describing tradeoffs and run instructions
- Basic Django project with one `Activity` model and a DRF endpoint returning activities

Labels: enhancement, architecture
