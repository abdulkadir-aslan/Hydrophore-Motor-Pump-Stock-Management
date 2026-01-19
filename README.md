# Hydrophore, Motor & Pump Stock Management

A Django-based system for managing the inventory and movement of hydrophores, motors, and pumps. Track entries, exits, maintenance, and workshop operations efficiently.

## Features

- User login and logout
- User authorization and roles
- Stock tracking for hydrophores, motors, and pumps
- Workshop entry/exit tracking
- Filtering and search
- Notifications for operations
- Custom forms and validations
- AJAX-powered dynamic selection for hydrophores
- Custom middleware for access control
- View-level permission decorators
- Custom template tags
- django-filter based advanced filtering

## Installation

1. **Clone the repository**

    ```sh
    git clone https://github.com/abdulkadir-aslan Hydrophore-Motor-Pump-Stock-Management
    cd hydrophore-stock-management
    ```

2. **Create a virtual environment and activate it**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**

    Copy `.env.example` to `.env` and configure your settings (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB, etc.)

5. **Run migrations**

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser to access the admin panel**

    ```sh
    python manage.py createsuperuser
    ```
    > After the user is created, log into the admin panel and ensure the user status is **Active**.

7. **Start the development server**

    ```sh
    python manage.py runserver
    ```

8. **Access the application**

    Open your browser and navigate to `http://127.0.0.1:8000/` to access the system.  
    Admin panel: `http://127.0.0.1:8000/admin/`.

---

## Project Structure

- `core/`: Main project directory.
  - `settings.py`: Project settings.
  - `urls.py`: URL routing.
  - `wsgi.py`: WSGI configuration.
  - `middleware/`: Custom middleware implementations
- `account/`: User management.
  - `admin.py`: Admin configuration.
  - `decorators/`: View-level permission decorators
  - `models.py`: User models.
  - `urls.py`: User-related URLs.
  - `views.py`: User views.
  - `forms.py`: User forms
- `homepage/`: Home/dashboard operations.
  - `views.py`: Home page views.
- `hydrophore/`: Hydrophore management.
  - `admin.py`
  - `models.py`
  - `views.py`
  - `forms.py`
  - `filters.py`
- `warehouses/`: Inventory management (motors, pumps).
  - `templatetags/`: Custom Django template tags
  - `admin.py`
  - `models.py`
  - `views.py`
  - `forms.py`
  - `filters.py`
- `media/`: Uploaded files (documents, images)
- `static/`: Static files (CSS, JS, images)
- `templates/`: Django HTML templates


---

## Static and Media Files

- `STATIC_URL`: URL for static files  
- `MEDIA_URL`: URL for uploaded media  
- `MEDIA_ROOT`: Directory for uploaded media  

---

## Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/en/5.2/)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
