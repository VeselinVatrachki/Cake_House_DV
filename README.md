# Cake House 🎂

A Django-based web application for managing cakes, categories, tags, and orders.

## Features
- Custom user model (`accounts.User`)
- Category, Tag, and Cake models
- Admin panel customization
- Static and media file handling
- Django REST Framework (optional)
- Responsive frontend with custom CSS

## Requirements
- Python 3.12+
- Django 6.0+
- pip / virtualenv

## Installation
```bash
git clone https://github.com/VeselinVatrachki/Cake_House_DV
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

## ⚙️ Configuration
Create a `.env` file in the root directory and add the following:
- `SECRET_KEY`
- `DATABASE_URL`
- `DEBUG`
- `REDIS_URL`

## 🛠️ Tech Stack
* **Backend:** Django 6.0
* **API:** Django Rest Framework
* **Task Queue:** Celery & Redis
* **Database:** PostgreSQL