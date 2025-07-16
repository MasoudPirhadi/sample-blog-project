# Sample Blog Project

**Sample Blog Project** is a simple bilingual (Farsi and English) blog website built with the Django framework. This project is designed as a starting point for personal or educational blog development and can be used as a foundation for larger projects.

## Features

- **Post Management**: Ability to create, edit, and delete posts by authors.
- **Comment System**: Users can post comments under articles.
- **Bilingual Support**: Supports both Farsi and English.
- **Django Admin Panel**: For managing content and users.
- **Modular Structure**: Uses separate apps for posts, comments, and user accounts.

## Prerequisites

To run this project, you need the following:

- Python 3.8 or higher
- Django 4.0 or higher
- MySQL or SQLite database
- Access to an SMS panel for sending notifications (if needed)

## Installation and Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MasoudPirhadi/sample-blog-project.git
   cd sample-blog-project
  

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   
4. **Set Up Environmental Settings
Copy the .env-example file to .env and configure the necessary settings, such as database and SMS credentials.**

   ```bash
   cp .env-example .env
   
5. **Run Migrations**
   ```bash
   python manage.py migrate
   
6. **Create Superuser**
   ```bash
   python manage.py createsuperuser

7. **Run the Server**
   ```bash
   python manage.py runserver
   
**Usage
Once the server is running, you can access the application at http://127.0.0.1:8000. To access the admin panel, go to http://127.0.0.1:8000/admin and log in with the superuser account.**
