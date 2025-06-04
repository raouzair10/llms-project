# 💼 BankBot – Domain-Specific AI Assistant for Banking Support

## 📌 Overview

BankBot is a secure, responsive, and domain-specific AI assistant designed for a local banking environment. Leveraging the power of Large Language Models (LLMs), vector search, and fine-tuning techniques, the assistant can understand and respond to customer queries based on curated datasets of anonymized interactions, FAQs, and policy documents.

This project simulates a real-world LLM application and provides hands-on experience with end-to-end deployment of AI assistants using open-source technologies.

---

## 🚀 Features

* 🔐 Guardrails to ensure data privacy and ethical AI interaction
* 🧠 Fine-tuned **LLaMA-3.2-3B-Instruct** model for domain relevance
* 🔎 Semantic search using **FAISS** and **Sentence Transformers**
* 📄 Real-time document ingestion and indexing
* 🌐 Interactive frontend using **Streamlit**
* 🛠️ RESTful backend API using **FastAPI**

---

## 🛠️ Tech Stack

### Languages & Frameworks

* **Python** – Core logic and scripting
* **PyTorch** – LLM fine-tuning backend
* **FastAPI** – Backend API service
* **Streamlit** – Frontend interface

### LLMs & Embeddings

* `meta-llama/Llama-3.2-3B-Instruct` – Base model
* `sentence-transformers` – Vector embedding generation
* `PEFT (LoRA)` – Lightweight fine-tuning

### Indexing & Retrieval

* **FAISS** – Vector similarity search engine
* **Pandas**, **json** – Preprocessing and data manipulation

### DevOps & Collaboration

* **Git & GitHub** – Version control and team collaboration
* **ngrok** – Public access to backend in development mode

---

## 🧩 System Architecture

1. **User Interaction Layer**: Submit queries or upload banking documents.
2. **Streamlit Frontend**: User-friendly UI for interaction.
3. **FastAPI Backend**: Handles /ask and /upload endpoints.
4. **Data Processing Pipeline**: Cleans, splits, and prepares documents.
5. **Vectorization Layer**: Embeds text using sentence-transformers.
6. **Retriever**: Fetches relevant content from FAISS index.
7. **LLM Reasoning**: Generates context-aware responses using LLaMA.
8. **Output & Guardrails**: Filters and returns safe, compliant responses.

---

## 📦 Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/raouzair10/llms-project.git
cd llms-project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Backend Server

```bash
# Optionally expose using ngrok
ngrok config add-authtoken <your_token>
ngrok http 8000  # Copy the public URL

# Run FastAPI backend
uvicorn backend:app --reload
```

### 4. Launch the Streamlit App

Update `app.py` with your ngrok URL:

```python
BASE_URL = "https://<your-ngrok-url>"
```

Then run:

```bash
streamlit run app.py
```

---

## 🧪 Using the Interface

* **Ask a Question**: Get real-time responses to banking queries.
* **Upload Documents**: Add new knowledge via PDFs or text files.
* The knowledge base updates dynamically as new documents are ingested.

---

## 📚 References

* [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)
* [FAISS: Facebook AI Similarity Search](https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/)
* [HuggingFace PEFT](https://github.com/huggingface/peft)
* [Streamlit](https://github.com/streamlit/streamlit)
* [PyTorch](https://github.com/pytorch/pytorch)

