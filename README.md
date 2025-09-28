# 🌸 Flower Space 🌸

**A Social Media Platform for Plant Lovers**

[Live Demo](https://flower-space-xi.vercel.app/)

---

## Table of Contents

* [Update Log](#update-log)
* [About](#about)
* [Features](#features)
* [Technology Stack](#technology-stack)
* [Installation](#installation)
* [License](#license)

---

## 📅 Update Log

### Latest Highlights

* **Account System Overhaul**

  * Email-based registration with OTP verification
  * Profile editing (name, avatar, bio)
  * Follow / Unfollow and Block logic with real-time counts
  * Relations manager have been added to manage your relations better. (followings, blocked, followers)
* **Bookmarks & Likes**

  * Redis-backed like and bookmark repositories for speed
  * Dedicated bookmarks page
* **Posts & Articles**

  * Cached homepage feed for faster loads
  * Inline hashtag creation when posting
  * Comment system with block-aware filtering
* **Earth News**

  * Daily plant/earth news fetched via BeautifulSoup and cached per day
* **Cart Manager**

  * Hybrid session/cache cart with auto-save and merge on login
* **Performance & UX**

  * Server-side caching of posts and daily quotes
  * More helpful flash messages and error handling

---

## 🌿 About

Flower Space is a vibrant social platform where plant enthusiasts share their botanical journeys, swap tips, and shop for plant-related products.
From daily plant quotes to real-time notifications and a small marketplace, Flower Space connects green thumbs everywhere.

---

## ✨ Key Features

### 🌱 Core Social

* Post creation with hashtags, multiple images, and optional comments
* Like & bookmark system with Redis for instant feedback
* Follow/unfollow users and manage relationships with block support
* Daily inspirational plant quotes

### 📰 Articles & News

* Community gardening articles
* “Earth News” section auto-scraped and refreshed daily

### 🛒 Shop

* Product listings with comments, ratings, discounts, and multiple images
* Hybrid cart (session + cache) that merges automatically after login

### 👤 Accounts

* Email/OTP registration and secure login
* Profile editing (name, avatar, bio)
* Relations manager page to view followers, followings, and blocked users

### 🔔 Notifications

* Real-time notifications for likes, comments, and coupon publications

---

## 🛠️ Technology Stack

**Backend**

* Django & Django ORM
* PostgreSQL
* Redis (likes, bookmarks, caching)
* BeautifulSoup & Requests (web scraping)
* ArvanCloud (media storage)
* Vercel (deployment)

**Frontend**

* HTML5, CSS3, JavaScript
* Font Awesome icons

---

## 📂 Installation

```bash
# 1. Clone
git clone https://github.com/yourusername/flower-space.git
cd flower-space

# 2. Virtual env
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Migrate database
python manage.py migrate

# 5. Run server
python manage.py runserver
```

Environment variables you’ll need:

* `SECRET_KEY`
* `DATABASE_URL` (or individual DB settings)
* `REDIS_URL`
* Email credentials for OTP sending

---

## 📜 License

MIT License – feel free to fork and build your own garden!

---


