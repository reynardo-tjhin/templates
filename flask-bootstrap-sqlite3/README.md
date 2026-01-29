# Flask-Bootstrap-SQLite3

- Tech stack
    - Backend: Flask with Jinja templates
    - Frontend: HTML/CSS with Bootstrap and JavaScript (to get data)
    - Database: SQLite3
- Benefits of using this Tech stack
    - Flask handles routing and sending templates for us (works as a server-side rendering)
    - Does not need to install CORS in the backend, etc.
    - Everything works within the same environment (or local host)
    - Deployment is easy and simple

## Setup

1. (Recommended) Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
    - `uv` is a high-performance python package manager that is build from Rust
    - `uv` helps to integrate package management (pip) and environment creation (virtual environment)
    - `uv` is also very easy to use!
2. Initialise the directory: `uv init`, it will create files like
    - `.python-version`
    - `main.py` - you can remove this
    - `pyproject.toml`
    - etc.
3. Install the dependencies
    - `uv add flask`
    - `uv add flask-wtf`: for CSRF protection
4. Add folders
    - `mkdir src` - source folder that contains the source codes/backend logic
    - `mkdir src\templates`
    - `mkdir src\static` - can also split into two folders (`mkdir static\css` and `mkdir static\js`)
5. Create some files
    - `src\__init__.py` - the app initialisation file
    - `src\db.py` - backend that connects to the database
    - `src\auth.py` - a simple authentication
    - `src\config.py` - the config file
    - `src\routes.py` - handle the routes
6. Create backend API folder
    - `mkdir src\api`
7. Create database schema
    - `src\schema.sql`
    - `src\dummy_data.sql`
8. Create configuration files
    - `config.ini`
    - `.env` - containing secrets, etc.