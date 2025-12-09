# Social Media API – Authentication Module

This project is the foundation of a Social Media API built using Django and Django REST Framework.

## Features

- Custom User Model
- Token-Based Authentication
- User Registration
- User Login
- User Profile Endpoint
- Followers Relationship (self-referencing ManyToMany)

---

Installation & Setup
Clone the Repository
Create a Virtual Environment
Install Dependencies
Apply Migrations
Run the Server

Authentication Endpoints
Register
POST `/api/accounts/register/`

Body:

```json
{ "username": "peter", "email": "peter@example.com", "password": "password123" }
```
