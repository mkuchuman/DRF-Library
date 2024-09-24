# DRF Library Project

## Overview

This project is a library system built with Django and Django Rest Framework (DRF). It provides an API for managing users, books, and book borrowing, and integrates with Stripe for rental and fine payments.

## Features

- User management (registration, authentication)
- Book management (CRUD operations)
- Book borrowing system
- Integration with Stripe for rental payments and overdue fines
- Support for periodic payments and reminders
- Task queuing with Django Q

## Technology Stack

- Python 3.12
- Django 5.1
- Django Rest Framework (DRF)
- Django Q (for task processing)
- Stripe API (for payments)

## Installation

### 1. Clone the repository

Clone the project from the repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```
### 2. Install dependencies

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```
### 3. Run the migrations:

```bash
python manage.py migrate
```
### 4. Stripe and Telegram configuration:
To enable payments with Stripe payments and Telegram notifications, edit .env.sample and rename ot into .env:
### 5. Run the development server
To start the development server:

```bash
python manage.py runserver
```

## Running with Docker
To run the project using Docker, execute the following command:

```bash
docker-compose up --build
```

## Usage
API Endpoints
The main API endpoints include:

api/users/ — User management

api/books/ — Book management

api/borrowings/ — Book

api/payments/ — Payments