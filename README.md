# Quest-Flask-FullStack

## Overview

This is a full-stack social media web application that offers content sharing and user engagement. It includes various features like secure payment processing for VIP subscriptions, Google Sign-In, Multi-Factor Authentication (MFA), role-based authorization, and more. This project showcases seamless integration of backend APIs with an interactive and aesthetic front-end.

## Features
- RESTful APIs for content sharing and user engagement
- Secure Payment processing for VIP subscription via Stripe API
- OAuth-based Google Sign-In
- Multi-Factor Authentication (MFA)
- Role-based authorization
- Interactive front-end data visualization

## Technologies Used
* Python
* Flask
* SQLAlchemy
* MySQL / SQLite
* Stripe API
* Google Sign-In (OAuth)
* Multi-Factor Authentication
* Front-end Dev Set (HTML, CSS, JavaScript)
* Jinja2
* Bootstrap
* Apache ECharts

## Installlation and Setup

1. Clone the repository
```bash
git clone <url>
```

2. Change into the project directory:
```bash
cd YourRepositoryName
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a .env file and populate it with necessary API keys and database credentials:
```python
STRIPE_API_KEY=your_stripe_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
DATABASE_URL=your_database_url
```

5. Migration
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run the Flask Server

```python
flask run
```

## Usage
Visit `http://127.0.0.1:5000` to access the application. 
Visit `http://127.0.0.1:5000` to access the application. 

# Contributing 
If you're interested in contributing, please fork the repository and create a pull request. For major changes, open an issue for discussion first.

# Contact
LinkedIn (Lexi Yin): https://www.linkedin.com/in/lexi-m-yin

