from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "meta-llama/Llama-3.2-3B-Instruct"

# Load model and tokenizer (from cache if downloaded already)
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")

# Input prompt
text_to_summarize = """
The Industrial Revolution, which began in Britain during the late 18th century, 
dramatically transformed the world. It marked a shift from agrarian economies to industrialized ones, driven by the invention of new machinery and techniques. 
The steam engine, invented by James Watt, enabled factories to operate more efficiently and fueled the expansion of railways, which revolutionized transport. 
Urban areas rapidly expanded as people migrated from rural villages in search of work, leading to overcrowded cities and the rise of working-class neighborhoods. 
Child labor, long working hours, and poor working conditions became prevalent in factories. Meanwhile, industrialists accumulated great wealth and new social classes emerged. 
This period also saw significant environmental degradation due to increased coal usage and deforestation. Despite the hardships, the Industrial Revolution laid the groundwork for technological progress, mass production, and modern economies.
"""

prompt = f"""
You are a helpful assistant. Read the text below and summarize it into a concise parahraph.

ONLY include information that is explicitly stated in the text. Do NOT add your own knowledge or make assumptions.

### Text:
{text_to_summarize}

### Paragraph Summary:
"""
# Tokenize and generate
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=200)

# Decode and print result
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
