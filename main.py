from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

app = FastAPI()

# Load model and tokenizer
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B-Instruct",
    device_map="auto",
    torch_dtype=torch.float16,
    use_auth_token=True  # <-- This line is required for gated models
)

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-3.2-3B-Instruct",
    use_auth_token=True  # <-- Same here
)

model = PeftModel.from_pretrained(base_model, "ahmedsaleha/nust-bank-llama3")

# Pydantic model for input
class QueryRequest(BaseModel):
    query: str

@app.post("/generate")
async def generate_answer(data: QueryRequest):
    prompt = f"<|user|>\n{data.query}\n<|assistant|>"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=256, do_sample=True, temperature=0.7)

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract only the model's answer (after the <|assistant|> tag)
    if "<|assistant|>" in answer:
        answer = answer.split("<|assistant|>")[-1].strip()

    return {"answer": answer}
