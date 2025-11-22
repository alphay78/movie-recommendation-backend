
# 🎬 Movie Recommendation Backend

![Django](https://img.shields.io/badge/Django-5.2.8-green?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=flat-square&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-orange?style=flat-square&logo=redis)
![Swagger](https://img.shields.io/badge/Swagger-UI-yellow?style=flat-square)

---

## 🔍 Overview

This project is the **backend for a Movie Recommendation App**, built to reflect real-world backend engineering with a focus on **performance**, **security**, and **scalability**.

The backend includes:

- Trending & recommended movie APIs (via TMDb)
- JWT-based user authentication
- Favorite movie storage
- Redis caching for performance
- Full Swagger documentation

---

## 🎯 Project Goals

- Develop APIs for trending and recommended movies  
- Authenticate users with JWT  
- Allow users to save favorite movies  
- Improve speed using Redis caching  
- Provide complete API documentation  

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| Django 5.2.8 | Backend development |
| PostgreSQL | Relational database |
| Redis | Caching layer |
| Swagger UI | API documentation |
| TMDb API | Third-party movie source |

---

## ✨ Key Features

### 1️⃣ Movie Recommendation APIs
- Fetch trending movies  
- Fetch personalized recommendations  
- TMDb data mapped to local DB  
- Handles missing or invalid TMDb data gracefully  

### 2️⃣ Authentication & Favorites
- JWT login + signup  
- Users can add/remove favorite movies  
- Favorites stored per user  

### 3️⃣ Redis Performance Boost
- Cache trending & recommended movies  
- Reduce TMDb API calls  
- Faster responses  

### 4️⃣ Swagger Documentation
Available at:  
👉 **http://127.0.0.1:8000/api/schema/swagger-ui/**  

---

## 🚀 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-repo/movie-recommendation-backend.git
cd movie-recommendation-backend
## 🚀 Installation & Setup

### 2️⃣ Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
### Install Dependencies
pip install -r requirements.txt
4️⃣ Create .env File

Create a file named .env in the project root and paste:
# Django Settings
SECRET_KEY=django-insecure-mq9v$6@p3*0#&b@2t1d+qf)r9r1m6y2a$8z!0d3^c&h+nq^#j7
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=movie_recommendation
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Redis Cache
REDIS_URL=redis://127.0.0.1:6379/0

# TMDB API
TMDB_API_KEY=6774205bc0d002816ee41a1b12988617
### 5️⃣ Run Migrations
python manage.py migrate
6️⃣ Start Redis (if running locally)
redis-server
### 7️⃣ Start Django Server
python manage.py runserver


