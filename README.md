# 🐦 TweetAssist AI

An AI-powered customer support intelligence system that uses Retrieval-Augmented Generation (RAG) to analyze social media complaints, classify urgency, and generate empathetic support responses.

---

## 🚀 Overview

**TweetAssist AI** helps support teams understand and respond to customer complaints at scale.

The system analyzes social media–style messages and automatically:

- 🔍 Understands the customer issue  
- ⚠️ Classifies urgency (Low / Medium / High)  
- ✉️ Generates professional support replies  
- 📊 Retrieves similar historical complaints  
- 🎛️ Enables analyst-side filtering and controls  

TweetAssist AI combines semantic search (Chroma) with a local LLM (Ollama) to produce grounded, context-aware responses.

---

## ✨ Key Features

- 🧠 **RAG-powered complaint analysis**
- 📊 **Semantic retrieval using Chroma vector DB**
- ⚠️ **Automatic urgency classification**
- 💬 **Empathetic reply generation**
- 🐦 **Twitter-style chat interface**
- 🎚️ **Dynamic Top-K retrieval control**
- 🔎 **Retrieved complaint transparency panel**
- 🚦 **Urgency-based filtering**
- ⚡ **Quick test prompt buttons**
- 🧩 **Sarcasm-aware tone handling**

---

## 🏗️ Architecture

```
User Query
   ↓
Chroma Vector Search
   ↓
Retrieved Complaint Context
   ↓
LLM Reasoning (Ollama)
   ↓
Structured Support Output
```

---

### 🧰 Tech Stack

- **Frontend:** Streamlit  
- **LLM Runtime:** Ollama (gemma3)  
- **Embeddings:** mxbai-embed-large  
- **Vector Database:** Chroma  
- **Language:** Python  

---

## 📂 Project Structure

```
.
├── main.py                     # Streamlit application
├── vector.py                   # Vector DB ingestion pipeline
├── chroma_support_db/          # Persisted vector store
├── Accuracy_Report.txt         # Evaluation results
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd tweetassist-ai
```

---

### 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
```

**Mac/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

### 3️⃣ Install dependencies

```bash
pip install streamlit langchain langchain-ollama langchain-chroma chromadb pandas
```

*(Or use requirements.txt if you create one.)*

---

### 4️⃣ Install and run Ollama

Pull required models:

```bash
ollama pull gemma3
ollama pull mxbai-embed-large
```

---

### 5️⃣ Build the vector database

Run once:

```bash
python vector.py
```

---

### 6️⃣ Launch the app

```bash
streamlit run main.py
```

---

## 🧪 Evaluation

TweetAssist AI was evaluated across diverse customer support scenarios:

- delayed deliveries  
- refund issues  
- account access failures  
- sarcasm detection  
- positive feedback cases  
- multi-issue complaints  

**Overall Accuracy Rating:** ⭐ **9.1 / 10**

See:

```
Accuracy_Report.txt
```

---

## 🎯 Example Use Cases

- Social media support monitoring  
- Support agent copilots  
- Customer experience analytics  
- Complaint triage systems  
- Helpdesk automation  

---

## 🔮 Future Improvements

- 🤖 Multi-agent critique layer  
- 🧠 Conversation memory  
- 📊 Urgency analytics dashboard  
- 🔁 Hybrid search (BM25 + vectors)  
- ⚡ Response streaming  

---

## 👤 Author
**SHAIK ABDULLAH AZAM**

Student project exploring real-world LLM + RAG applications for customer support intelligence.

---

## ⭐ Acknowledgements

- LangChain  
- Ollama  
- Chroma  
- Streamlit  
- Twitter Customer Support Dataset  
