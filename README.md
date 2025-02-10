### **Abstract: CryBIT - AI-Powered Real-Time Scam Detection System**

CryBIT is an advanced, **AI-powered scam detection system** designed to monitor and analyze messages on **Telegram** in real-time. The system leverages **Machine Learning (ML), Natural Language Processing (NLP), and pattern-based techniques** to detect and flag fraudulent content, such as cryptocurrency scams, phishing links, and fake investment schemes. CryBIT is built using **Flask** for the backend, **Telethon** for Telegram integration, and **MongoDB** for data storage. It features a **real-time risk scoring system**, an **interactive UI**, and **dynamic configuration options**, making it a powerful tool for preventing financial fraud.

The core of CryBIT lies in its **multi-layered scam detection logic**, which combines **ML-based text classification**, **NLP semantic similarity matching**, **keyword-based detection**, **phishing URL detection**, **crypto wallet blacklist checks**, and **OCR-based text extraction**. Each detection technique contributes to a **cumulative risk score**, which is compared against a **configurable threshold** to determine if a message is a scam. If the risk score exceeds the threshold, the message is flagged, stored in MongoDB, and displayed in the **dashboard** for further analysis. Admins are also alerted in real-time via Telegram.

CryBIT's **scoring system** is designed to be **flexible and accurate**. Each detection method adds a specific weight to the risk score:

- **ML Model Prediction**: Adds `+0.6` to the score.
- **Keyword Match**: Adds `+0.5`.
- **Phishing URL Detected**: Adds `+0.6`.
- **Crypto Wallet Blacklist Match**: Adds `+0.7`.
- **OCR Text Match**: Adds `+0.3`.

The **total risk score** is calculated as the sum of these weights. If the score exceeds the **risk threshold** (default: `0.4`), the message is flagged as a scam. This multi-layered approach ensures high accuracy and minimizes false positives.

CryBIT's **modular architecture** ensures scalability and ease of maintenance. The system is divided into several modules, including **configuration management**, **utility functions**, **Flask backend**, **scam detection logic**, **Telegram monitoring**, and **database integration**. The **interactive UI** allows users to manage monitored channels, view flagged messages, and customize scam detection settings.

---

### **Block Diagram of CryBIT System Architecture**

Below is a block diagram illustrating the architecture of CryBIT:

Copy

```
+-------------------+       +-------------------+       +-------------------+
|   Telegram        |       |   CryBIT System   |       |   MongoDB         |
|   Channels        |<----->|   (Flask Backend) |<----->|   Database        |
+-------------------+       +-------------------+       +-------------------+
                                   |       ^
                                   |       |
                                   v       |
                          +-------------------+
                          |   Interactive UI  |
                          |   (HTML, AJAX)    |
                          +-------------------+
```

---

### **Flowchart of CryBIT Workflow**

The flowchart below explains the step-by-step workflow of CryBIT:

1. **Start**: CryBIT starts monitoring Telegram channels.
2. **Fetch Messages**: Telethon fetches new messages from monitored channels.
3. **Analyze Message**: The message is analyzed using multiple detection techniques.
4. **Calculate Risk Score**: Each detection method contributes to the risk score.
5. **Check Threshold**: If the risk score > threshold, flag the message as a scam.
6. **Store in MongoDB**: Flagged messages are stored in the database.
7. **Update UI & Send Alerts**: The dashboard is updated, and admins receive alerts.
8. **Repeat**: The process repeats for new messages.

Copy

```
+-------------------+
|    Start          |
+-------------------+
         |
         v
+-------------------+
| Fetch Messages    |
| (Telethon)        |
+-------------------+
         |
         v
+-------------------+
| Analyze Message   |
| (ML, NLP, etc.)   |
+-------------------+
         |
         v
+-------------------+
| Calculate Risk    |
| Score             |
+-------------------+
         |
         v
+-------------------+
| Risk Score >      |
| Threshold?        |
+-------------------+
         |
         v
+-------------------+       +-------------------+
| Yes: Flag Message |       | No: Ignore Message |
+-------------------+       +-------------------+
         |
         v
+-------------------+
| Store in MongoDB  |
+-------------------+
         |
         v
+-------------------+
| Update UI & Send  |
| Alerts            |
+-------------------+
         |
         v
+-------------------+
| Repeat for Next   |
| Message           |
+-------------------+
```

---

### **Detailed Explanation of the Scoring System**

The **risk scoring system** in CryBIT has been updated to provide **greater accuracy and flexibility**. Here's how it works:

1. **Keyword-Based Detection**:
    - The system checks the message against a list of **scam-related keywords** (e.g., "free bitcoin", "double your money").
    - If a keyword match is found, it adds `+0.5` to the risk score.
    - **Example**: If the message contains "free bitcoin", the risk score increases by `0.5`.
2. **ML Model Prediction**:
    - A **pre-trained ML model** (e.g., RandomForest) analyzes the text of the message using a **TF-IDF vectorizer**.
    - The model predicts the probability of the message being a scam (`prediction`).
    - The prediction value is added directly to the risk score.
    - If the prediction exceeds `0.3`, the message is flagged with "ML Model Prediction".
    - **Example**: If the model predicts a `0.6` probability, the risk score increases by `0.6`.
3. **NLP Semantic Analysis**:
    - The system uses **Sentence Transformers** (e.g., `all-MiniLM-L6-v2`) to generate embeddings for the message.
    - The mean value of the embedding tensor is calculated.
    - If the mean value exceeds `0.1`, it adds `+0.2` to the risk score.
    - **Example**: If the embedding mean is `0.15`, the risk score increases by `0.2`.
4. **Phishing URL Detection**:
    - The system checks any URLs in the message using the **Google Safe Browsing API**.
    - If a phishing URL is detected, it adds `+0.6` to the risk score.
    - **Example**: If the URL is flagged as phishing, the risk score increases by `0.6`.
5. **Crypto Wallet Blacklist Check**:
    - The system verifies any cryptocurrency wallet addresses in the message against a **blacklist**.
    - If a blacklisted wallet is found, it adds `+0.7` to the risk score.
    - **Example**: If the wallet is blacklisted, the risk score increases by `0.7`.
6. **OCR-Based Text Extraction**:
    - If the message contains an image, the system uses **EasyOCR** to extract text from the image.
    - The extracted text is analyzed using the same detection techniques.
    - If a scam is detected, it adds `+0.3` to the risk score.
    - **Example**: If the extracted text contains a scam keyword, the risk score increases by `0.3`.
7. **Total Risk Score**:
    - The scores from all detection methods are summed up to calculate the **total risk score**.
    - If the total score exceeds the **risk threshold** (default: `0.4`), the message is flagged as a scam.
    - **Example**: If the total risk score is `0.8`, the message is flagged as a scam.

---

### **Code Files for Understanding the Logic**

To better understand the logic, you can upload the following code files:

1. **`scam_detection.py`**: Contains the core logic for scam detection and risk scoring.
2. **`telethon_integration.py`**: Handles Telegram message fetching and monitoring.
3. **`database.py`**: Manages MongoDB operations for storing and retrieving flagged messages.
4. **`main.py`**: Flask backend with routes and API endpoints.
5. **`config.json`**: Configuration file with API keys, Telegram credentials, and scam detection settings.

---

### **Conclusion**

CryBIT is a **cutting-edge scam detection system** that combines **AI, real-time monitoring, and an interactive UI** to protect users from financial fraud. Its **multi-layered detection logic** and **flexible scoring system** ensure high accuracy and adaptability. With CryBIT, users can stay one step ahead of scammers and safeguard their investments.
