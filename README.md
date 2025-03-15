# 🌸 Flower Space 🌸

**A Social Media Platform for Plant Lovers**

[See demo here](https://theartificialflower.pythonanywhere.com/)
## NOTE: 
**PYTHON ANYWHERE IS BEING A BITCH. SO THE OTP SYSTEM DOES NOT WORK BUT THE CONTACT US PERFECTLY WORKS!! ALSO THE DEMO USES MYSQL INSTEAD OF POSTGRES DUE TO PYTHONANYWHERE ISSUES. USE "testuser@email.com" AS EMAIL AND "testuser" AS PASSWORD TO LOG IN!!!**

## 🌿 About

Flower Space is a vibrant social media platform designed for plant enthusiasts to share their botanical journeys, connect with fellow gardeners, and grow their green communities. From sharing plant photos to discussing gardening tips, Blossom Connect brings nature lovers together.

## ✨ Features

### 🌱 Core Features
- **Post Creation**: Share your plant photos with descriptions and hashtags
- **Likes & Comments**: Engage with other users' posts
- **Bookmarks**: Save your favorite posts for later
- **Articles**: Read and share gardening articles
- **User Profiles**: Showcase your plant collection and gardening expertise
- **OnlineShop**: A simple yet detailed onlineshop where you can order beatiful flowers!! (AI WIP)

### 🌸 Advanced Features
- **Real-time Notifications**: Stay updated with likes and comments
- **Hashtag System**: Discover content through tags
- **Profile Customization**: Edit your profile picture and bio
- **Follow System**: Connect with other plant lovers
- **Admin Order Management**: change clients' order status, with a search bar and sort by options.
- **2 step verification**: A code will be sent to your email whenever you try to register an account.
- **Advanced Cart**: Saves your products in your sessions even if you are not logged in!
  

## 🛠️ Technology Stack

### Backend
- **Django**: Python web framework
- **PostgresSQL**: Relational database


### Frontend
- **HTML5 & CSS3**: Responsive design with custom animations
- **JavaScript**: Interactive UI components
- **Font Awesome**: Beautiful icons


### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/blossom-connect.git
   cd blossom-connect
   ```

2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up database: (After editing settings)
   ```bash
   python manage.py migrate
   ```

5. Run development server:
   ```bash
   python manage.py runserver
   ```
