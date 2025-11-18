# 🧠 Coderr – Marketplace & Review Management API

A **Django REST Framework** based backend for managing orders, offers, user profiles, and reviews.  
Users can create offers, place orders, review business users, and manage their profiles.  
This project provides a **fully functional REST API** ready to connect to a frontend (e.g., Angular, React, or Vue).

---

## 🚀 Features
- 🔐 User authentication via token (login/register)
- 💼 Offers management (create, update, list ...etc.)
- 🛒 Orders linked to offers and users
- 🌟 Reviews for Business Users (prevent duplicate reviews)
- 🧑‍💻 User profiles with editable information for Customers and Business Users
- ⚙️ REST API endpoints for easy frontend integration

---

## 🧰 Requirements

Before starting, make sure you have:

| Requirement | Description |
|--------------|-------------|
| **Python ≥ 3.10** | Required to run Django |
| **pip** | Python’s package manager |
| **git** | To clone this repository |
| **virtualenv** *(optional but recommended)* | To isolate project dependencies |

---

## 💻 Setup Instructions (All Operating Systems)

The following steps work on **Windows, macOS, and Linux**.

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/KanMind.git
cd KanMind
```

### 2️⃣ Create a virtual environment
#### 🪟 On Windows
```
python -m venv venv
venv\Scripts\activate
```
#### 🍎 On macOS / Linux
```
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Set up the database
Create all required tables:
```
python manage.py makemigrations
python manage.py migrate

```

### 5️⃣ Create a superuser (admin)
```
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.


### 6️⃣ Run the development server
```
python manage.py runserver
```
and open: 
```
http://127.0.0.1:8000/
```
---

## 🧩 Project Structure
```
Coderr_project-Adel/
│
├── order_app/ # Orders app
│ ├── models.py # Order models
│ ├── api/
│ ├── serializers.py # Serializers for orders
│ ├── views.py # CRUD logic for orders
│ ├── permissions.py # Custom order permissions
│ ├── urls.py # App-specific order routes
│
├── offer_app/ # Offers app
│ ├── models.py # Offer models
│ ├── api/
│ ├── serializers.py
│ ├── views.py
│ ├── permissions.py
│ ├── urls.py
│
├── review_app/ # Reviews app
│ ├── models.py
│ ├── api/
│ ├── serializers.py
│ ├── views.py
│ ├── permissions.py
│ ├── urls.py
│
├── profile_app/ # User profiles app
│ ├── models.py
│ ├── api/
│ ├── serializers.py
│ ├── views.py
│ ├── permissions.py
│ ├── urls.py
│
├── coderr_core/ # Main project settings
│ ├── settings.py # Global configuration
│ ├── urls.py # Root URL routes
│
├── user_auth_app/ # Authentication app
│ ├── api/
│ ├── serializers.py
│ ├── views.py
│ ├── permissions.py
│ ├── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔑 Authentication
This project uses **Token Authentication**.
After registering or logging in, you’ll receive a token like:
``` json
{
  "token": "f2b2f69d3e314cbbd1a2b06a6fxyzabcd"
}
```
Include it in your headers for all API requests.

---

## 🔗 Example API Endpoints

| Method | Endpoint                          | Description                                           |
| ------ | --------------------------------- | --------------------------------------------------- |
| `POST` | `/api/register/`                  | Register new user                                    |
| `POST` | `/api/login/`                     | Log in and get token                                 |
| `GET`  | `/api/offers/`                    | List all offers                                      |
| `POST` | `/api/offers/`                    | Create a new offer                                   |
| `GET`  | `/api/offers/<id>/`               | Get offer details                                    |
| `GET`  | `/api/orders/`                    | List all orders for the authenticated user          |
| `POST` | `/api/orders/`                    | Place a new order                                    |
| `GET`  | `/api/orders/<id>/`               | Get details of a specific order                      |
| `GET`  | `/api/reviews/`                   | List reviews made by or for the user                |
| `POST` | `/api/reviews/`                   | Create a new review (one per user/business)         |
| `GET`  | `/api/profiles/<id>/`             | Retrieve a user's profile                            |
| `PATCH`| `/api/profiles/<id>/`             | Update profile information                           |

---

## 🧪 Testing the API

You can test all endpoints using:
- Postman
- Insomnia
- Django’s built-in API browser

---