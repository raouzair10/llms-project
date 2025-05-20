import nest_asyncio
import threading
from pyngrok import ngrok
import uvicorn
import re
from fastapi import FastAPI, Request, File, UploadFile, Form
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import numpy as np
from typing import List
from io import BytesIO
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

#inference Model
model_path = "/content/llama3-qa-finetuned"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)


#Load the embeddings &  FAISS index
embeddings = np.load("nust_bank_embeddings.npy")
index = faiss.read_index("faiss_index.idx")
# Load the corresponding texts
texts_path = "/content/indexed_docs.json"
with open(texts_path, "r") as f:
    texts = json.load(f)

embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda' if torch.cuda.is_available() else 'cpu')

#Define retriever
def retrieve_relevant_chunks(query, top_k=3):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [texts[i] for i in indices[0]]

#Generate answer from context + query
def generate_answer_from_context(query):
    context_chunks = retrieve_relevant_chunks(query)
    context = "\n".join(context_chunks)
    instruction = """You are a helpful, polite customer service agent for NUST Bank. Answer the customer's question clearly and concisely using the relevant information below. Do not explain your reasoning. Just give a direct, informative paragraph.\n\n"""


    prompt = f"{instruction}Context:\n{context}\n\nQuestion: {query}\nAnswer:"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        do_sample=True,
        top_p=0.9,
        eos_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(output[0], skip_special_tokens=True).split("Answer:")[-1].strip()

#Anonymization
def anonymize_text(text: str) -> str:
    #Mask emails
    text = re.sub(r'\b[\w.-]+?@\w+?\.\w+?\b', '[EMAIL]', text)
    # Mask phone numbers (very simple pattern)
    text = re.sub(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b', '[PHONE]', text)
    #Mask simple names (e.g., capitalized words) — crude but illustrative
    text = re.sub(r'\b[A-Z][a-z]{1,}\b', '[NAME]', text)
    #Add more patterns as needed
    return text


#create FastAPI Aapp
app = FastAPI()

class QueryRequest(BaseModel):
    query: str

#Generate answer 
@app.post("/generate")
async def generate_answer(req: QueryRequest):
    query = anonymize_text(req.query)
    answer = generate_answer_from_context(query)
    return {"answer": answer}

#upload DOCs
@app.post("/upload/")
async def upload_file(
    username: str = Form(...),
    uploaded_file: UploadFile = File(...)
):
    #Save uploaded file
    save_dir = Path("saved_files")
    save_dir.mkdir(parents=True, exist_ok=True)
    file_path = save_dir / uploaded_file.filename

    with open(file_path, "wb") as f:
        f.write(await uploaded_file.read())

    #Load uploaded JSON QA data
    with open(file_path, "r") as f:
        new_data = json.load(f)

    if not isinstance(new_data, list):
        return {"error": "Uploaded file must contain a list of question-answer dictionaries."}

    new_qa_format = [f"Q: {entry['question']}\nA: {entry['answer']}" for entry in new_data]
    
    #Generate new embeddings
    new_embeddings = np.array(embedding_model.encode(new_qa_format, convert_to_tensor=False)).astype('float32')
    faiss.normalize_L2(new_embeddings)

    global texts, index

    #Update RAG state
    texts += new_qa_format
    if index is None:
        embedding_dim = new_embeddings.shape[1]
        index = faiss.IndexFlatIP(embedding_dim)
    index.add(new_embeddings)

    return {
        "message": f"✅ File '{uploaded_file.filename}' uploaded by '{username}' and integrated into RAG.",
        "total_entries": len(texts)
    }

#Uvicorn setup
nest_asyncio.apply()
public_url = ngrok.connect(8000)
print(f"Your FastAPI app is live at: {public_url}")

threading.Thread(target=uvicorn.run, args=(app,), kwargs={"host": "0.0.0.0", "port": 8000}).start()


