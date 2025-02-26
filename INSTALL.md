# Installation Instructions for Netfix

## Prerequisites
- Python 3.x
- pip
- Django

## Steps to Install
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd netfix
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. Open your web browser and navigate to `http://127.0.0.1:8000/`.
