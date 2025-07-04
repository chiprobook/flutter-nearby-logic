# flutter-nearby-logic
displaying content related to your current location, translating longitude and latitude into plaintext
# 🏡 HouseAgentApp

![Python](https://img.shields.io/badge/Language-Python-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.0.0-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

![Demo Screenshot](assets/demo.png) <!-- Replace with your image path -->

---

## 📘 Overview

**HouseAgentApp** is a Python-powered application housed in `housing.py`, designed to help users discover nearby houses, shortlets, and properties based on their current location. By combining geolocation and reverse geocoding with SQLite queries, it delivers personalized housing suggestions inside a dynamic and user-friendly interface.

---

## 🚀 Features

- 📍 Detects user's city/street via IP geolocation
- 🗺️ Reverse geocoding with fallback logic
- 🧮 Distance filtering using haversine formula
- 🏡 Displays nearby houses, shortlets, and properties
- 🖼️ UI components with housing image previews and details
- 🔙 Navigation support with a floating back button
- ⚡ Interactive click-through to reveal full property info

---

## 🔧 Technologies

- **Python**  
- **Geocoder**  
- **SQLite**  
- **Custom UI Framework Components:**  
  `Container`, `Row`, `Column`, `ListView`, `Image`, `Text`, `FloatingActionButton`, `Icons`

---

## 🛠 Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/chiprobook/flutter-nearby-logic.git
   cd flutter-nearby-logic

2. Install dependencies:
   pip install geocoder

Database Schema
Your SQLite database should include three tables:

🔹 house_details
🔹 shortlet_details
🔹 property_details

Each table must contain:
id INTEGER,
title TEXT,
location TEXT,
price TEXT,
images TEXT,
latitude REAL,
longitude REAL,
street TEXT

images is expected to be a JSON-encoded list of image URLs.
latitude and longitude are used for proximity calculations.

🧪 Usage
Run housing.py inside your app framework and initiate the nearby search:

python
agent.houses_nearby(event)
This function:

Retrieves user’s IP-based coordinates

Performs reverse geocoding for city/street info

Dynamically filters nearby properties from the SQLite database

Renders listings using custom UI with clickable image cards

Results include:

Title, location, price

Distance from user in kilometers

Street info and image preview

Interactive containers for detailed view callbacks

📜 License
This project is licensed under the MIT License. See LICENSE for usage and distribution terms.

🤝 Contribution
Pull requests and suggestions are welcome! Feel free to fork, improve filtering logic, redesign the UI, or add new features.

👨‍💻 Author
Built with 💚 by Reginald 📫 Contact: chiprobook@hotmail.com


