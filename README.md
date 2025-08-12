# coderr-backend

# Coderr Backend

Coderr Backend is a Django-based REST API for a marketplace platform. It provides user management, offer listings, order processing, and review functionality. The project is organized into modular Django apps for scalability and maintainability.

## Features

- User registration, authentication, and profile management
- Marketplace offers and offer details
- Order creation and management
- Review and rating system
- RESTful API endpoints (Django REST Framework)
- Modular app structure for easy extension

## Project Structure

```
core/                # Django project settings and configuration
marketplace_app/     # Marketplace logic: offers, orders, reviews
users_app/           # User management: registration, profiles
requirements.txt     # Python dependencies
manage.py            # Django management script
```

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ereit673/coderr-backend.git
   cd coderr-backend
   ```

2. **Create a virtual environment (optional but recommended):**

   **macOS/Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows (Command Prompt):**

   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```bash
   python3 manage.py migrate
   ```

5. **Run the development server:**

   ```bash
   python3 manage.py runserver
   ```

6. **Run tests:**
   ```bash
   python3 manage.py test
   ```

## API Overview

- All API endpoints are organized under `/marketplace_app/api/` and `/users_app/api/`.
- Authentication is required for most endpoints (see permissions in code).
- See serializers and views in each app for detailed API structure.
