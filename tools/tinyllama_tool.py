
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
llm = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=256)

def tinyllama_tool(query):
    prompt = f"<|system|>\nYou are a helpful assistant.\n<|user|>\n{query}<|assistant|>"
    output = llm(prompt)[0]["generated_text"]
    response = output.split("<|assistant|>")[-1].strip()
    return response, 0.6  # conservative confidence