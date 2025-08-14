# ☀️ Smart Solar Power Management System

An intelligent web application built with **Python** and **Streamlit** to forecast solar power generation and help users manage their electricity load efficiently.  
This project uses a **Machine Learning model** (`RandomForestRegressor`) to make real-time predictions.  

---

## ✨ Key Features

🔮 **Live Power Prediction** – Predicts real-time solar power output in both **Watts (W)** and **Kilowatts (kW)** based on weather conditions.  

⚙️ **Personalized System Setup** – Allows users to input their **solar panel wattage** and **quantity** for predictions tailored to their setup.  

🔌 **Dynamic Load Management** – Interactive calculator to select home appliances from a dropdown and check if the current power generation can support the electrical load.  

📊 **Daily Performance Forecast** – Visualizes the estimated power generation curve over the day (**6 AM – 6 PM**) with an interactive line chart.  

💰 **Savings Calculator** – Estimates daily **monetary savings** based on total power generated & local electricity unit price.  

---

## 🛠 Tech Stack

- 🐍 **Language**: Python  
- 🌐 **Web Framework**: Streamlit  
- 🤖 **Machine Learning**: Scikit-learn  
- 📊 **Data Handling**: Pandas, NumPy  
- 💾 **Model Persistence**: Joblib  

---

## 🚀 Project Setup & Installation

1️⃣ **Clone the Repository**  
  ```bash
git clone https://github.com/Ahmad-beast/solarpanel.git
cd solarpanel
  ```
---
## 2 Install Dependencies

**Run this to install requirements**
  ```bash
pip install -r requirements.txt
  ```
---  
## 3 Run the App
**To Run the APP (This is for MACOS)**
  ```bash
python3 -m streamlit run app.py```
---
