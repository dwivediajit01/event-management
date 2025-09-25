
# Event Management

This is a Django-based event management project containing two main apps:

- `eventapp` — event and attendee models, views, forms, templates.
- `authapp` — custom authentication (email or username login), signup/login views and templates.

Project layout (important files/folders):

- `Del/` — Django project package (contains `settings.py`, `urls.py`, `wsgi.py`, `manage.py`).
- `eventapp/`, `authapp/` — the main Django apps.
- `templates/` — global templates (base, home, navbar).
- `static/` and `media/` — static assets and uploaded media (profile pictures).
- `db.sqlite3` — default SQLite database file (committed in this repo).
- `populated_emp.py` — a data population script (inspect before running).

Quickstart (Windows / PowerShell)

1. Install Python 3.11+ and Git if you don't already have them.

2. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create a `.env` file at the repository root with environment-specific secrets. Example `.env` keys used by the project:

```
DJANGO_SECRET_KEY=replace-with-a-secret
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

The repository's `.gitignore` already excludes `.env`. Do not commit secrets.

5. Run database migrations and create a superuser:

```powershell
python Del\manage.py migrate
python Del\manage.py createsuperuser
```

6. Run the development server:

```powershell
python Del\manage.py runserver
```

7. Open http://127.0.0.1:8000 in your browser.

Notes and tips

- Django version: the project was created using Django 5.2.1 (see `Del/Del/settings.py` header). If you need to match exactly, the `requirements.txt` pins Django to 5.2.1.
- The settings import `python-dotenv` to load `.env` values. Make sure `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are set in your `.env` if you plan to send email.
- `db.sqlite3` is included in the repo. If you prefer a fresh database, remove or move `db.sqlite3` before running `migrate`.
- Static files are served from `static/` during development; uploaded media files are stored under `media/`.
- There's a small helper script `populated_emp.py` at the repo root — inspect it before running.

Running tests

```powershell
python Del\manage.py test
```

Useful management commands

- `python Del\manage.py makemigrations` — create migrations for model changes.
- `python Del\manage.py migrate` — apply migrations.
- `python Del\manage.py createsuperuser` — create admin user.
- `python Del\manage.py collectstatic` — collect static files (for production deployment).

Assumptions

- This README assumes you're using Python 3.11 or newer and running on Windows PowerShell (project files show bytecode for CPython 3.13 in the workspace, so adjust if you use a different interpreter).

Security

- Remove or rotate any real credentials found in repository files. The project currently contains example email settings in `Del/Del/settings.py` — replace those with values in your `.env` and *do not commit* them.

Further steps (suggested)

- Add a `requirements.txt` (done) or `pyproject.toml` to fully capture dependencies.
- Add a CONTRIBUTING.md with developer workflow and testing guidelines.
- Add CI (GitHub Actions) that runs `python -m pip install -r requirements.txt` and `python Del\manage.py test` on push.

If you'd like, I can also:

- Add a more detailed `CONTRIBUTING.md` and `DEV_ENV.md` for onboarding.
- Create a `Dockerfile` and `docker-compose.yml` for local development.

---

Happy hacking — open an issue or tell me which follow-up you'd like next.
