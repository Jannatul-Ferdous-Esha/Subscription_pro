# 🧾 Subscription Management System

A **Django-powered** application to manage user subscriptions with **real-time USD→BDT currency exchange tracking**. This project features a user-friendly REST API, background exchange rate logging using **Celery**, and a clean web interface for managing and viewing subscriptions.

---

## ⚙️ How It Works

### 🔗 Core Components

- **Backend**: Django + Django REST Framework  
- **Asynchronous Tasks**: Celery with Redis  
- **External API**: Currency exchange via [exchangerate-api]  
- **Database**: MySQL   
- **Frontend**: Django templates with Bootstrap  
- **Admin Panel**: Django admin for managing subscriptions and plans  

---

## 📦 Features in Detail

### 1. Subscription Plans

Admins can create and manage various subscription plans via the admin panel. Each plan includes:

- Name  
- Price (in USD)  
- Duration (in days)  

Stored in the `Plan` model.

---

### 2. User Subscriptions

Authenticated users can subscribe to any available plan. Each subscription includes:

- Associated user and plan  
- Start and end date  
- Status (`active`, `cancelled`, or `expired`)  

Automatically updated upon expiration or cancellation.

---

### 3. Background Task with Celery

A periodic Celery task runs **every hour** to:

- Fetch current USD→BDT exchange rate  
- Save it to the `ExchangeRateLog` model  

**Message broker**: Redis  
**Scheduler**: Celery Beat  

To run Celery:

```bash
celery -A subscription worker -l info
celery -A subscription beat -l info
```

---

### 4. Admin Panel

Visit `/admin/` (superuser login required) to:

- Create/edit/delete subscription plans  
- Manage user subscriptions  
- View historical exchange rates  

---

### 5. Frontend Interface

Public-facing subscription list at `/subscriptions/`:

- Username  
- Plan Name  
- Start Date  
- End Date  
- Status  

Built with Bootstrap 5 and Django templates. No login required.

---

### 6. Docker (Optional)

The project supports containerization with `Dockerfile` and `docker-compose.yml`.

**Services**:

- Django web server  
- Redis (for Celery)  
- MySQL (for data persistence)  

To run:

```bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## ✅ Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/Jannatul-Ferdous-Esha/Subscription_pro.git
cd Subscription_pro
```

### Step 2: Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 4: Apply Migrations

```bash
python manage.py migrate
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server

```bash
python manage.py runserver
```

---

## 🧪 Technologies Used

- Django 5.x  
- Django REST Framework  
- Celery  
- Redis  
- MySQL  
- Bootstrap 5  
- Docker 

---

## 👩‍💻 Author

**Jannatul Ferdous Esha**  
📧 jannatul.ferdous.esha11235@gmail.com  
🔗 [GitHub Profile](https://github.com/Jannatul-Ferdous-Esha)
