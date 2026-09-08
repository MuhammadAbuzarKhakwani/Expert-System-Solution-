# Library Django App (Week-3 DAY-5)

This is a small Django library application used for Week-3 exercises. It provides:

- Book listing, create, edit, delete
- Borrow and return functionality with per-user borrow records
- Simple auth (login/register)

Quickstart

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

2. Install requirements

```bash
pip install -r requirements.txt
```

3. Run migrations

```bash
python manage.py migrate
```

4. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

5. Run the development server

```bash
python manage.py runserver
```

Notes

- Templates are in `books/templates/` and shared base in `templates/base.html`.
- Database is SQLite (`db.sqlite3` in the project folder).
