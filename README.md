# Furniture Store Setup Guide

## Steps to Run the Furniture Store Project

### Step 1: Clone the Repository
```sh
git clone <repository_url>
cd <repository_name>
```

### Step 2: Create and Activate Virtual Environment
Before creating a virtual environment, ensure you have Python 3.12 installed on your system.
If Python 3.12 is not installed, download and install it from the official link: [Python Downloads](https://www.python.org/downloads/)

Create a virtual environment and activate it:
```sh
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows
```

### Step 3: Install Dependencies
```sh
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the project root directory and configure the required environment variables.

#### Cloudinary Setup (For Media Storage)
Create an account on [Cloudinary](https://cloudinary.com/) and get the following credentials:
```env
CLOUD_NAME=<your_cloudinary_name>
CLOUDINARY_API_KEY=<your_cloudinary_api_key>
CLOUDINARY_API_SECRET=<your_cloudinary_api_secret>
```

#### Django Secret Key
Generate a Django secret key using the following command:
```sh
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Add the generated key to your `.env` file:
```env
DJANGO_SECRET_KEY=<your_django_secret_key>
```

#### Razorpay Setup (For Payments)
Create a [Razorpay](https://razorpay.com/) test account and obtain the API credentials:
```env
RAZORPAY_KEY=<your_razorpay_key>
RAZORPAY_KEY_SECRET=<your_razorpay_secret>
```

#### PostgreSQL Database Setup
Sign up on [Neon.tech](https://console.neon.tech/) to create a PostgreSQL database and obtain the credentials:
```env
DB_NAME=<your_database_name>
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
DB_HOST=<your_database_host>
PORT=5432
```

#### Email Configuration
Make sure you have two-factor authentication enabled on your Google account. You will need to generate an app password from Google using the following link:
[Google App Passwords](https://myaccount.google.com/apppasswords)
```env
EMAIL_HOST_USER=<your_email_user>
EMAIL_HOST_PASSWORD=<your_email_app_password>
```

#### Set Environment to Production
For local development, set `DEBUG=True`. For production, ensure `DEBUG=False`.
```env
DJANGO_ENV='production'
DEBUG=False  # Change to True in local development
```

### Step 5: Load Environment Variables in the Project
Ensure you import and load environment variables in the following files:
- `config/settings/base.py`
- `config/settings/production.py`
- `views/checkout_view.py`

Add the following lines at the top of these files to load environment variables from .env file. If already present, uncomment them:
```python
from dotenv import load_dotenv
load_dotenv()
```

Also, make sure to add the allowed hosts configuration in `config/settings/production.py`:
```python
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
```

### Step 6: Run the Project
Once all setup is complete, start the Django server:
```sh
python3 manage.py runserver
```
The project will now be accessible locally.
