# Crypto Backtesting Tool

## 📌 Overview
This repository provides a Python-based **crypto trading backtesting tool** that allows users to test different trading strategies using historical OHLC (Open, High, Low, Close) data from CoinGecko.

## 🚀 Features
- **Moving Average Crossover Strategy** (`ma-crossover`)
- **ATR (Average True Range) Strategy** (`atr`)
- Supports multiple cryptocurrencies
- Saves backtesting results as `.png` plots
- Compares strategy performance vs **Buy & Hold**

---
## 🔧 Installation Guide

### **1️⃣ Create a GitHub Account (If Needed)**
If you don't have an account, sign up at [GitHub](https://github.com/).

### **2️⃣ Install Dependencies**
Ensure you have **Git & Python** installed:

- **Windows**: Install [Git](https://git-scm.com/downloads) & [Python](https://www.python.org/downloads/)
- **Mac/Linux**: Run:
  ```sh
  sudo apt install git python3 python3-venv -y   # Ubuntu/Debian
  sudo dnf install git python3                   # Fedora
  brew install git python3                       # macOS (Homebrew)
  ```

### **3️⃣ Clone This Repository**
In **VS Code Terminal** (`Ctrl+~`):
```sh
git clone https://github.com/haanjohn/crypto-backtest.git
cd crypto-backtest
```

### **4️⃣ Set Up Python Virtual Environment**
```sh
python3 -m venv venv
```
Activate it:
- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```sh
  source venv/bin/activate
  ```

### **5️⃣ Install Required Libraries**
```sh
pip install -r requirements.txt
```

---
## 📊 Running Backtests
Run backtests with different strategies:

### **Moving Average Crossover Strategy**
```sh
python backtest.py bitcoin --strategy ma-crossover --short 10 --long 50
```

### **ATR Strategy**
```sh
python backtest.py bitcoin --strategy atr --atr-multiplier 2
```

### **Results:**
- Generates a `.png` file with backtest results
- Prints final portfolio values compared to **Buy & Hold**

---
## 💡 Contributing
If you'd like to contribute:
1. **Fork this repo** & create a new branch:
   ```sh
   git checkout -b my-feature
   ```
2. **Make changes, commit, & push:**
   ```sh
   git add .
   git commit -m "Added a new feature"
   git push origin my-feature
   ```
3. **Open a Pull Request** on GitHub 🚀

---
## 📬 Contact
For questions, feel free to open an **Issue** or reach out!

---
### 🏆 Happy Backtesting!
