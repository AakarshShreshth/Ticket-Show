# Ticket Show

### Description
Ticket Show is a simple ticket booking application designed for multiple users  to book tickets for various movies and shows with ease.

### Technologies Used
1. **Flask**: A Python-based web framework that is lightweight and easy to use.
2. **Jinja**: A template engine that creates dynamic web pages for the app interface.
3. **SQLite**: A relational database that stores the app data.
4. **Flask-Login**: An extension that handles user sessions and authentication.
5. **Werkzeug-Security**: A utility that generates and verifies secure password hashes for the database.
6. **Flask Packages**: A collection of modules that provide various functionalities for the app, such as request handling, template rendering, flash messages, URL generation, redirection, and response creation.

### Features
1. **Book tickets**: Users can book tickets for various events and shows, such as concerts, plays, movies, etc.
2. **Search shows and venues**: Users can search for shows and venues by location, date, price, category, and rating.
3. **View show details**: Users can view the details of each show, such as description, duration, cast, reviews, and availability.
4. **Manage bookings**: Users can manage their bookings and cancel or modify them if needed. They can also view their booking history and print or download their tickets.
5. **Admin panel**: Admins can create, modify, and delete venues and shows. They can also view and edit the bookings and users of the app.

### How to Run

Clone the project

```bash
git clone https://github.com/AakarshShreshth/Ticket-Show.git
```

Go to the project directory

```bash
cd Ticket-Show
```

Create Virtual Environment

```bash
python -m venv .env
```

Start Virtual Environment

```bash
source .env/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the application

```bash
python app.py
```
