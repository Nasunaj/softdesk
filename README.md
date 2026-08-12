# SoftDesk API
A RESTful API (buid with Django REST Framework) for managing projects, tasks (issues), comments, and users.
---
## Prerequisites
- Python 3.12+
- Pipenv (recommended for dependency management) 
---
## Installation
### 1. Clone the repository:
````
git clone https://github.com/Nasunaj/softdesk.git
cd softdesk
````
---
### 2. Create a virtual environment
```bash
pipenv install
```

#### 3. Activate the virtual environment

  ```bash
  pipenv shell
  ```
---

### 4. Configure environment variables

Create a `.env` file at the root of the project to store sensitive variables (such as the Django secret key). Here is an example of its content:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

To generate a secret key, you can use [this online generator](https://djecrety.ir/) or run the following Python code:
 ```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
---
### 5. Apply migrations

Django uses migrations to manage the database. Run the following commands to create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Run the Development Server

Start the Django server with the following command:

```bash
python manage.py runserver
```

> **Access the Application**:
> - Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Project Structure
Here is an overview of the project structure:
```
softdesk/
├── users/               # User management (authentication, profiles)
├── projects/            # Project and contributor management
├── issues/              # Issue and comment management
├── softdesk/            # Django configuration (settings, URLs)
├── .env                 # Environment variables (SECRET_KEY, etc.)
├── Pipfile              # Python dependencies
└── README.md            # This file
```
---

## Authentification
### Create account
To create a new user, send a POST request to /api/signup/ with the following data:
```json
{
    "username": "your_username",
    "email": "your_email@example.com",
    "password1": "your_password",
    "password2": "your_password",
    "age": 25,
    "can_be_contacted": false,
    "can_data_be_shared": false
}
```
### Get a JWT Token
To authenticate, send a POST request to /api/token/ with your credentials:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
Response :
```json
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}
```
Use the access token in the Authorization header for authenticated requests:
```text
Authorization: Bearer your_access_token
```
---

## API Endpoints
### Users
| Endpoint | Method    | Description | Permissions |
| --- |-----------| --- | --- |
| /api/signup/ | POST      | Create a new user account | Public |
| /api/token/ | POST      | Get JWT tokens (login) | Public |
| /api/token/refresh/ | POST      | Refresh the access token | Authenticated |
| /api/users/ | GET       | List all users | Admin only |
| /api/users/{id}/ | GET       | Retrieve a specific user | Authenticated (self) or Admin |
| /api/users/{id}/ | PUT/PATCH | Update a user | Authenticated (self) or Admin |
| /api/users/{id}/ | DELETE    | Delete a user | Admin only |

### Projects
| Endpoint | Method    | Description | Permissions |
| --- |-----------| --- | --- |
| /api/projects/ | GET       | List all projects (user's projects) | Authenticated |
| /api/projects/ | POST      | Create a new project | Authenticated |
| /api/projects/{id}/ | GET       | Retrieve a specific project | Contributor or Author |
| /api/projects/{id}/ | PUT/PATCH | Update a project | Author only |
| /api/projects/{id}/ | DELETE    | Delete a project | Author only |

### Contributors
| Endpoint | Method | Description | Permissions |
| --- | --- | --- | --- |
| /api/contributors/ | GET | List all contributors (user's projects) | Authenticated |
| /api/contributors/ | POST | Add a contributor to a project | Project Author only |
| /api/contributors/{id}/ | DELETE | Remove a contributor from a project | Project Author only |

### Issues
| Endpoint | Method    | Description | Permissions |
| --- |-----------| --- | --- |
| /api/issues/ | GET       | List all issues (user's projects) | Authenticated |
| /api/issues/ | POST      | Create a new issue | Contributor |
| /api/issues/{id}/ | GET       | Retrieve a specific issue | Contributor |
| /api/issues/{id}/ | PUT/PATCH | Update an issue | Issue Author only |
| /api/issues/{id}/ | DELETE    | Delete an issue | Issue Author only |
| /api/issues/?include=comments | GET       | List issues with nested comments | Authenticated |

### Comments
| Endpoint | Method    | Description | Permissions |
| --- |-----------| --- | --- |
| /api/comments/ | GET       | List all comments (user's projects) | Authenticated |
| /api/comments/ | POST      | Create a new comment | Contributor |
| /api/comments/{id}/ | GET       | Retrieve a specific comment | Contributor |
| /api/comments/{id}/ | PUT/PATCH | Update a comment | Comment Author only |
| /api/comments/{id}/ | DELETE    | Delete a comment | Comment Author only |
---
## Testing the API

Postman or CURL can be used for example to test the API

---
## Green Code & Optimisation
- Pagination : all endpoints support pagination (10 items per page).
- Controlled nesting : use `?include=comments` to fetch nested data only when needed.
- Optimisation queries : use `selected_related` and `perfetch_related` to avoid N+1 query issues.