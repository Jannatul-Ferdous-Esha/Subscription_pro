🧾 Subscription Management System
A Django-powered application to manage user subscriptions with real-time USD→BDT currency exchange tracking. It includes user-friendly APIs, background rate logging via Celery, and a clean web interface to display subscriptions.

⚙️ How It Works
🔗 Core Components
Backend: Django + Django REST Framework

Asynchronous Tasks: Celery with Redis

External API: Currency exchange rates (via exchangerate-api or similar)

Database: MySQL 

Frontend: Basic Bootstrap template (non-SPA)

Admin Panel: Django admin site for managing plans and logs

📦 Features in Detail
1. Subscription Plans
Admin users can create subscription plans via the admin panel. Each plan has:

A name

A price (in USD)

A duration (in days)

Plans are stored in the Plan model.

2. User Subscriptions
Authenticated users can subscribe to a plan. Each subscription:

Links a user to a plan

Has a start date, end date, and status

Status updates when cancelled or expired

Subscriptions are stored in the Subscription model. Subscriptions are created atomically using transaction.atomic() to ensure data integrity.

3. Background Task with Celery
A periodic task runs every hour:

Fetches the current USD → BDT rate

Stores the value in the database (ExchangeRateLog)

This is implemented in tasks.py using Celery and scheduled using Celery Beat. Redis is used as the message broker.

To run:

bash
Copy code
celery -A subscription worker -l info
celery -A subscription beat -l info
4. Admin Panel
Navigate to /admin/ as a superuser.

From there, you can:

Add/edit/delete subscription plans

View or manage all user subscriptions

Browse the history of exchange rate logs

5. Frontend Interface
Go to /subscriptions/ to see a public-facing HTML table listing:

Username

Plan

Start Date

End Date

Status

This page uses Bootstrap and Django templates. No login is required to view this list.

6. Docker (Optional)
If included in your repo:

The app supports containerization via Dockerfile and docker-compose.yml.

Services:

Django web server

Redis for Celery

MySQL for persistent storage

Steps to run:

bash
Copy code
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

✅ Setup Instructions
Step 1: Clone the Repo
bash
Copy code
git clone https://github.com/Jannatul-Ferdous-Esha/Subscription_pro.git
cd Subscription_pro
Step 2: Create & Activate Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
Step 3: Install Requirements
bash
Copy code
pip install -r requirements.txt
Step 4: Apply Migrations
bash
Copy code
python manage.py migrate
Step 5: Create Superuser
bash
Copy code
python manage.py createsuperuser
Step 6: Run Server
bash
Copy code
python manage.py runserver

 Technologies Used
Django 5.x

Django REST Framework

Celery

Redis

MySQL 

Bootstrap 5

Docker 

 Author
Jannatul Ferdous Esha
