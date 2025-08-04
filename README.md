#!/bin/bash

cat << 'EOF' > README.md
# 🧾 Subscription Management System

A Django-powered application to manage user subscriptions with real-time USD→BDT currency exchange tracking.  
It includes user-friendly APIs, background rate logging via Celery, and a clean web interface to display subscriptions.

---

## ⚙️ How It Works

### 🔗 Core Components
- **Backend:** Django + Django REST Framework  
- **Asynchronous Tasks:** Celery with Redis  
- **External API:** Currency exchange rates (e.g., exchangerate-api.com)  
- **Database:** MySQL  
- **Frontend:** Basic Bootstrap template (non-SPA)  
- **Admin Panel:** Django admin site for managing plans and logs  

---

## 📦 Features in Detail

### 📌 Subscription Plans
Admin users can create subscription plans via the admin panel. Each plan has:
- A **name**
- A **price** (in USD)
- A **duration** (in days)

Plans are stored in the \`Plan\` model.

---

### 👤 User Subscriptions
Authenticated users can subscribe to a plan. Each subscription:
- Links a user to a plan
- Has a **start date**, **end date**, and **status**
- Status updates when cancelled or expired

Subscriptions are stored in the \`Subscription\` model and are created using \`transaction.atomic()\` to ensure data consistency.

---

### ⏳ Background Task with Celery

A periodic task runs every hour:
- Fetches the current USD → BDT exchange rate
- Stores the value in the \`ExchangeRateLog\` model

This is implemented in \`tasks.py\` using Celery and scheduled via Celery Beat. Redis is used as the message broker.

To run the workers:
\`\`\`bash
celery -A subscription worker -l info
celery -A subscription beat -l info
\`\`\`

---

### 🛠 Admin Panel

Visit \`/admin/\` (as a superuser) to:
- Add/edit/delete subscription plans
- View/manage user subscriptions
- Browse exchange rate logs

---

### 🌐 Frontend Interface

Visit \`/subscriptions/\` to view a public HTML table listing:
- Username
- Plan
- Start Date
- End Date
- Status

Built with Bootstrap + Django templates. No login required.

---

### 🐳 Docker (Optional)

If Docker is used, the project supports:
- **Django App**
- **Redis** (for Celery)
- **MySQL** (or SQLite)

To run:
\`\`\`bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
\`\`\`

---

## ✅ Setup Instructions (Local without Docker)

### Step 1: Clone the Repo
\`\`\`bash
git clone https://github.com/Jannatul-Ferdous-Esha/Subscription_pro.git
cd Subscription_pro
\`\`\`

### Step 2: Create & Activate Virtual Environment
\`\`\`bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
\`\`\`

### Step 3: Install Requirements
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 4: Apply Migrations
\`\`\`bash
python manage.py migrate
\`\`\`

### Step 5: Create Superuser
\`\`\`bash
python manage.py createsuperuser
\`\`\`

### Step 6: Run Server
\`\`\`bash
python manage.py runserver
\`\`\`

---

## 🧪 Technologies Used
- Django 5.x  
- Django REST Framework  
- Celery  
- Redis  
- MySQL  
- Bootstrap 5  
- Docker (optional)

---

## 🙋‍♀️ Author

**Jannatul Ferdous Esha**  
🔗 [GitHub Profile](https://github.com/Jannatul-Ferdous-Esha)
EOF
