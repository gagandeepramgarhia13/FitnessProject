# Fitness Tracker

A full-stack Django-based Fitness Tracker that helps users monitor their daily nutrition intake, track meals, manage food entries, and view calorie and macronutrient consumption over time.

## Features

### User Authentication

* User Registration
* User Login & Logout
* Secure Password Handling
* User-specific data isolation

### Food Tracking

* Add foods to Breakfast, Lunch, Dinner, and Snacks
* Track Calories, Protein, Carbohydrates, Fat, and Fibre
* Search foods from a built-in nutrition database
* Quantity-based nutrition calculation
* Edit food entries
* Delete food entries

### Nutrition Database

* Large food database containing common foods
* Supports Indian and international food items
* Nutritional values stored locally
* Fast food lookup without external APIs

### Daily Diary

* View daily food intake
* Navigate between different dates
* Review previous meal history
* Daily nutrition summaries

### Analytics

* Total Calories Consumed
* Total Protein Intake
* Total Carbohydrates Intake
* Total Fat Intake
* Total Fibre Intake

### Admin Panel

* Manage users
* Manage food database
* Manage food entries
* Built-in Django administration dashboard

---

## Tech Stack

### Backend

* Django 4.2
* Python

### Database

* PostgreSQL (Production)
* SQLite (Development)

### Deployment

* Render

### Frontend

* HTML
* CSS
* JavaScript
* Bootstrap

---

## Live Demo

https://fitness-tracker-lre0.onrender.com

---

## Installation

### Clone Repository

```bash
git clone https://github.com/MRILLEGAL725/Fitness-Tracker-capstone-project.git

cd Fitness-Tracker-capstone-project
```

### Create Virtual Environment

```bash
python -m venv fit
```

### Activate Virtual Environment

Windows:

```bash
fit\Scripts\activate
```

Linux / Mac:

```bash
source fit/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

### Import Food Database

After running migrations, import the food data from the CSV file:

```bash
python manage.py shell
```

Then run:

```python
exec(open("tracker/import_foods.py").read())
```

You should see a message indicating that the import completed successfully.

Verify the import:

```python
from tracker.models import FoodDatabase

print(FoodDatabase.objects.count())
```

The output should show the number of food items imported.

Type:

```python
exit()
```

to leave the Django shell.


### Create Superuser

```bash
python manage.py createsuperuser
```

### Start Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Project Structure

```text
fitness-tracker/
│
├── manage.py
├── requirements.txt
├── Procfile
│
├── fitnesstracker/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── tracker/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── import_foods.py
│
├── templates/
├── static/
├── foods.csv
```

---

## Deployment

This application is deployed on Render using:

* PostgreSQL Database
* Gunicorn
* WhiteNoise
* Environment Variables

Required Environment Variables:

```env
SECRET_KEY=your_secret_key

DATABASE_URL=your_postgresql_database_url
```

---

## Future Improvements

* Weight Tracking
* Goal-Based Nutrition Planning
* Barcode Scanner
* Meal Recommendations
* Weekly Analytics
* Monthly Reports
* Mobile App Version
* AI Meal Suggestions



## Author

**Vishal (MRILLEGAL725)**

* Cybersecurity Enthusiast
* Python Developer
* Full Stack Django Developer

GitHub:
https://github.com/MRILLEGAL725

---

## License

This project is created for educational and portfolio purposes.
# FitnessProject
