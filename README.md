# MineSweeperEngine  

This project is an **AI-powered Minesweeper bot** that plays the **Minroob League** game on Telegram. The bot automatically **analyzes the game board**, **identifies mines and safe moves**, and **plays optimally** using logic-based strategies.  

## 📌 Features
- **Automatic Minesweeper Gameplay**: Reads the board, decides the next move, and plays automatically.  
- **Game State Analysis**:  
  - Identifies **certain mines** and **safe moves** based on **neighboring numbers**.  
  - Detects **high-probability mine locations**.  
  - Stores **game progress** for future analysis.  
- **Telegram Bot Integration**:  
  - **Reads game states** from Telegram messages.  
  - **Interacts with Minroob League automatically**.  
- **Data Storage**:  
  - Saves **game history** in `data_saver/` for future improvements.  
  - Uses `config.json` in `target/` for **API credentials and settings**.  
- **Multi-game Support**: Can **handle multiple games** at once.  

---

## 🏗️ Project Structure
```
MineSweeperEngine/
│── data_saver/           # Stores game states for analysis
│   ├── {GameID}/         # Each game has a separate folder
│   │   ├── 01.json       # Step 1 of the game
│   │   ├── 02.json       # Step 2 of the game, and so on...
│── target/               # Configuration files
│   ├── config.json       # API credentials and settings
│── .gitignore            # Files to exclude from Git
│── requirements.txt      # Dependencies
│── classes.py            # Minesweeper logic
│── main.py               # Telegram bot integration
│── README.md             # Documentation
```

---

## 📂 Setting Up Directories  
Before running the bot, create the required folders:  

```bash
mkdir data_saver
mkdir target
```

---

## ⚙️ Configuring `config.json`  
The `config.json` file inside `target/` contains **API credentials** and **Telegram settings**.

```json
{
  "api_id": "YOUR_TELEGRAM_API_ID",
  "api_hash": "YOUR_TELEGRAM_API_HASH",
  "target1": "-100XXXXXXXXXX",  
  "admin": "123456789" 
}
```

### **Explanation of Fields**
- **`api_id`**: Your **Telegram API ID** (get it from [my.telegram.org](https://my.telegram.org/)).  
- **`api_hash`**: Your **Telegram API Hash**.  
- **`target1`**: The **chat ID** of **Minroob League bot**.  
- **`admin`**: Your **Telegram user ID** for **admin control**.  

**🚨 The bot’s identity is determined by the PDI character (first name of the Telegram account), which is retrieved dynamically. It is NOT stored in `config.json`.**  

---

## 🔧 Installation  
1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/yourusername/MineSweeperEngine.git
cd MineSweeperEngine
```

2️⃣ **Install Dependencies**  
```bash
pip install -r requirements.txt
```

3️⃣ **Create Config File**  
```bash
nano target/config.json
```
*(Copy-paste the JSON structure above and fill in your details.)*

---

## 🚀 Running the Bot  
Start the bot with:  
```bash
python main.py
```

---

## 🔍 How It Works  
### **1️⃣ Game State Extraction**
- The bot **reads the Minesweeper board** from Telegram messages.  
- Converts the **emoji-based game board** into a structured format.  

### **2️⃣ Logical Decision Making**
- **Identifies guaranteed moves**:  
  - Detects **safe spaces** and **certain mines** using **neighbor analysis**.  
  - If multiple moves are possible, selects **strategically**.  

### **3️⃣ Making Moves**
- The bot **interacts with Telegram’s UI** to **play automatically**.  

---

## 🏗️ Development & Future Plans  
✅ **Current Features**:
- **Automatic move selection** using **logical rules**.  
- **Game state tracking** for analysis and improvements.  
- **Support for multiple games**.  

🚀 **Planned Features**:
- **Probability-based move selection** for **better decision-making** in uncertain situations.  
- **Advanced AI to detect and counter opponent strategies**.  
- **Performance tracking & optimization reports**.  

---

## 📧 Contact & Support  
For questions, contributions, or bug reports, feel free to reach out!  

📌 **Developed for Minroob League Auto-Play using AI**  