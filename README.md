# 🩺 GesundLotse – AI-Powered Clinical Chat Assistant

**GesundLotse** is an empathetic, evidence-based medical guidance assistant that simulates a real doctor’s consultation style.  
It combines **retrieval-augmented generation (RAG)**, **PubMed (NCBI)** data lookup, and **web search** to provide safe, structured, and context-aware health advice.

⚠ **Disclaimer:** This tool does **not** replace professional medical care. For emergencies, always call your local emergency number.

---

## ✨ Features

- **Doctor-style Interview Flow** – Starts with 1–4 adaptive, clinically relevant questions before giving advice.
- **Evidence-Driven Guidance** – Uses PubMed (via NCBI API) and trusted clinical guidelines.
- **RAG Pipeline** – Retrieves relevant context from your indexed medical documents stored in Pinecone.
- **Web Search Integration** – Fetches recent and relevant public health information using the Serper API.
- **Multilingual Support** – Automatically detects German or English and responds accordingly.
- **Session Memory** – Remembers conversation history for contextual follow-ups.
- **Beautiful Web UI** – Clean, responsive chat interface with an empathetic intro card.

---

## 🏗 Architecture
```
├── app.py # Flask app with chat routes
├── src/
│ ├── helper.py # File loading, text splitting, search utilities
│ ├── ncbi.py # NCBI PubMed API integration
│ ├── prompt.py # System prompt & behavior rules
│
├── store_index.py # Script to index local medical documents into Pinecone
├── chat.html # Frontend chat interface
├── style.css # Chat UI styling
├── requirements.txt # Python dependencies
├── Dockerfile # Containerization
└── setup.py # Packaging metadata

```



## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_SECRET_KEY=your_flask_secret
HF_TOKEN=your_huggingface_api_token
PINECONE_API_KEY=your_pinecone_api_key
SERPER_API_KEY=your_serper_api_key
NCBI_API_KEY=your_ncbi_api_key   # optional
````

---

## ⚙ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/gesundlotse.git
cd gesundlotse
```

### 2️⃣ Install dependencies

```bash
pip install --no-cache-dir -r requirements.txt
```

### 3️⃣ Index your medical documents

Place your `.pdf`, `.txt`, or `.json` files inside a `data/` folder, then run:

```bash
python store_index.py
```

### 4️⃣ Run the app

```bash
python app.py
```

The app will be available at **[http://localhost:7860](http://localhost:7860)**

---

## 🐳 Docker Deployment

Build and run using Docker:

```bash
docker build -t gesundlotse .
docker run -p 7860:7860 --env-file .env gesundlotse
```

---

## 💻 Usage

1. Open the app in your browser.
2. The assistant will greet you with a short introduction.
3. Type your symptoms or health concern.
4. Answer 1–4 short follow-up questions.
5. Receive a structured, safe, and actionable response with red-flag warnings.

---

## 📌 Example Query

**User:** "I have a fever and cough for 3 days."
**Assistant:**

* Asks about duration, other symptoms, travel history.
* Provides possible causes, OTC advice, and when to seek urgent care.
* Includes PubMed research snippet & recent health updates.


## 📜 License

MIT License © 2025 Shreyash Manohar Deokate


