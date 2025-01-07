# **Django Boilerplate**

This project provides a ready-to-use boilerplate for Django application.
---

## **Project Setup**

### **Prerequisites**

Ensure you have the following installed:
- Python 3.10.12
- PostgreSQL
- pip (Python package installer)
- venv
---

### **Installation Steps**

### **1. Clone the Repository**

Start by cloning the repository to your local machine:

```bash
git clone git@github.com:mihiraj-ciphernutz/CN-Python-Starter.git
cd django-boilerplate
```

### **2. Create Venv for project**
you can create venv anywhere in your system

```bash
python3 -m venv venv
```

Activate the virtual environment:
- **On macOS/Linux**

```bash
source venv/bin/activate
```

### **3. Install Dependencies**
Install the required Python packages listed in the requirements.txt file:

Activate the virtual environment:

```bash
pip install -r requirements.txt
```

### **4. Setup PostgreSQL Database**
You will need a PostgreSQL database. Create a new database named django_boilerplate, and update the database connection credentials in settings.py under the DATABASES section.

```bash
DATABASES = {
    'default' : dj_database_url.parse(os.getenv('DATABASE_URL'))
}
```
here you have to put DATABASE_URL in .env and add .env it in .gitignore

### **5. Run Migrations**
Run Django migrations to set up the database schema:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

here you can if you want to revert migration from database schema

```bash
python3 manage.py migrate <app_name> <migration_name>
```

if you want to create empty migration file

```bash
python3 manage.py makemigrations <app_name> --empty --name <migration_name>
```

### **6. Run the Development Server**
Once everything is set up, start the Django development server:

```bash
python3 manage.py runserver
```

Your application will be accessible at http://127.0.0.1:8000.