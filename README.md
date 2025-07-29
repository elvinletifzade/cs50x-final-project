# Reminder

#### 🎥 Video Demo: <https://youtu.be/YOUR_VIDEO_URL>
#### 👨‍💻 Author: Elvin Lətifzada
#### 📅 Final Project for Harvard CS50x

---

**Reminder** is a full-featured subscription tracking web application built using Flask and SQLite. It helps users stay on top of their monthly and yearly service payments — such as domains, hosting, or software — through a clean, color-coded dashboard and reminder management tools.

---

## ✨ Features Overview

- 🔐 **User Authentication**
  - Register/login/logout system using session and hashed passwords.

- ➕ **Add Reminders**
  - Set title, frequency (`monthly` or `yearly`), and due date.

- 🎨 **Color-Coded Dashboard**
  - Automatically highlights urgency based on days left:
    - 🔴 Red: ≤ 10 days
    - 🟡 Yellow: 11–20 days
    - 🔵 Blue: 21–30 days
    - ⚪ Gray: > 30 days

- 🔍 **Live Search**
  - Instantly filter reminders via AJAX-based dynamic search by title.

- ✏️ **Edit Reminders**
  - Easily update reminder title, frequency, or due date.

- 🗑️ **Delete Reminders**
  - Confirmation modal to prevent accidental deletion.

- 👤 **Profile Page**
  - Change your username and password from the profile page.

- 📱 **Mobile-Friendly UI**
  - Built with **Bootstrap 5.3** for a smooth responsive layout.

---

## 🧰 Tech Stack

| Layer       | Technology |
|-------------|------------|
| Backend     | Python, Flask, CS50’s SQL wrapper |
| Frontend    | HTML5, CSS3, Bootstrap 5.3, Vanilla JS |
| Database    | SQLite |
| Auth        | Flask Session + Werkzeug Hashing |

---

## 🗃️ Database Schema

### `users` table
| Field    | Type     | Description               |
|----------|----------|---------------------------|
| id       | INTEGER  | Primary Key               |
| username | TEXT     | Unique username           |
| hash     | TEXT     | Password (hashed)         |

### `reminders` table
| Field      | Type      | Description                       |
|------------|-----------|-----------------------------------|
| id         | INTEGER   | Primary Key                       |
| user_id    | INTEGER   | FK → users(id)                    |
| title      | TEXT      | Name of the service               |
| frequency  | TEXT      | "monthly" or "yearly"             |
| due_date   | DATE      | When the next payment is due      |
| created_at | TIMESTAMP | Auto-generated timestamp          |

---

## 📁 Folder Structure

project/
│
├── app.py                # Main Flask app
├── helpers.py            # Utility functions
├── schema.sql            # DB schema (users, reminders)
├── requirements.txt      # pip install -r requirements.txt
├── reminder.db           # SQLite database file (generated at runtime)
│
├── static/
│   ├── styles.css        # Custom styling and color classes
│   └── main.js           # AJAX search & modal logic
│
├── templates/
│   ├── layout.html       # Shared layout
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   ├── dashboard.html    # Reminder list (main dashboard)
│   ├── reminder_table.html # AJAX search result partial
│   ├── add.html          # Add new reminder
│   ├── edit.html         # Edit existing reminder
│   └── profile.html      # User profile page (change username/password)


## 📝 Notes on Development Process
As a full-stack developer with over 10 years of experience in both backend and frontend technologies — including PHP, Node.js, React, Next.js, Angular, and Flutter — I approached this project not just as a coursework requirement, but also as a chance to create something functional and efficient within the CS50 framework.

Thanks to my background in algorithmic thinking and familiarity with a wide range of languages and frameworks, I was able to plan, structure, and implement the application quickly and confidently.

That said, I did use ChatGPT in a supporting role throughout the development process — primarily to streamline repetitive tasks, clarify certain syntax rules, and bounce ideas for code structure and implementation.

---
❗ However, all critical decisions, system design, business logic, and final implementation were entirely my own. ChatGPT served as a productivity tool, not a replacement for original work or problem-solving.
---

This reflects a real-world development approach, where experienced engineers leverage modern tools and assistants to speed up workflows — while retaining full responsibility and authorship over their code.

