# llm.py
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList, TextIteratorStreamer
import torch
import threading
from build_JSON_prompt import build_JSON_prompt
import json
import re


model_id = "meta-llama/Llama-3.2-3B-Instruct"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
model.to(device)


class StopOnStringAfterPrompt(StoppingCriteria):
    def __init__(self, tokenizer, stop_string, prompt_length):
        super().__init__()
        self.tokenizer = tokenizer
        self.stop_string = stop_string
        self.buffer = ""
        self.prompt_length = prompt_length

    def __call__(self, input_ids, scores, **kwargs):
        if input_ids.shape[1] <= self.prompt_length:
            return False
        # Decode only the new token to keep memory usage low
        new_token_id = input_ids[0, -1].item()
        self.buffer += self.tokenizer.decode([new_token_id], skip_special_tokens=True)

        return self.stop_string in self.buffer
    
def generate_summary(prompt, mode = "summary"):
    stop_string = "=== End of Output ==="
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    prompt_len = inputs['input_ids'].shape[1]
    
    
    output = model.generate(**inputs, max_new_tokens=500, do_sample=False, 
                            temperature=0.0, top_p=1.0, num_beams=1, eos_token_id=tokenizer.eos_token_id,
                            stopping_criteria=StoppingCriteriaList([
                                StopOnStringAfterPrompt(tokenizer, stop_string, prompt_len)]),)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    print(response)
    
    if mode == "summary":
        marker = "=== Summary ==="
    elif mode == "adjusted":
        marker = "=== Revised Summary ==="
    else:
        raise ValueError("Invalid mode. Use 'summary' or 'adjusted'.")
    
    # Find all occurrences of marker
    summary_markers = [i for i in range(len(response)) if response.startswith(marker, i)]
    
    if len(summary_markers) < 5:
        return response.strip()  # fallback if fewer than 5 summaries exist

    # Get the start of the actual 5th summary
    start_index = summary_markers[4] + len(marker)
    summary_part = response[start_index:]

    # Stop at the next "=== End of Output ==="
    end_marker_index = summary_part.find("=== End of Output ===")
    if end_marker_index != -1:
        summary_part = summary_part[:end_marker_index]

    return summary_part

def stream_summary(prompt: str, stop_string: str = "=== End of Output ==="):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    prompt_len = input_ids.shape[1]

    streamer = transformers.TextIteratorStreamer(
        tokenizer, skip_prompt=True, skip_special_tokens=True
    )

    generation_kwargs = {
        "input_ids": input_ids,
        "max_new_tokens": 500,
        "temperature": 0.0,
        "top_p": 1.0,
        "do_sample": False,
        "eos_token_id": tokenizer.eos_token_id,
        "streamer": streamer
    }

    # Run in background thread so we can yield results
    import threading
    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    buffer = ""
    for token in streamer:
        buffer += token
        if stop_string in buffer:
            yield buffer[:buffer.index(stop_string)]
            break
        else:
            yield token
            
def convert_to_JSON(table_rows):
    
    prompt = build_JSON_prompt(table_rows)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    prompt_len = inputs['input_ids'].shape[1]
    stop_string = "=== End of Output ==="
        
    output = model.generate(**inputs, max_new_tokens=1000, do_sample=False, 
                                temperature=0.0, top_p=1.0, num_beams=1, eos_token_id=tokenizer.eos_token_id,
                                stopping_criteria=StoppingCriteriaList([
                                    StopOnStringAfterPrompt(tokenizer, stop_string, prompt_len)])
                                )
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    marker = "JSON:"
        
        # Find all occurrences of marker
    summary_markers = [i for i in range(len(response)) if response.startswith(marker, i)]
        
    if len(summary_markers) < 7:
        response.strip()  # fallback if fewer than 5 summaries exist

    # Get the start of the actual 5th summary
    start_index = summary_markers[6] + len(marker)
    summary_part = response[start_index:]

    # Stop at the next "=== End of Output ==="
    end_marker_index = summary_part.find("=== End of Output ===")
    if end_marker_index != -1:
        summary_part = summary_part[:end_marker_index]

    print(summary_part)
    
    
    # Find all JSON arrays in the output
    json_blocks = re.findall(r'\[\s*{.*?}\s*\]', summary_part, re.DOTALL)
    
    # Parse each block separately
    parsed_blocks = [json.loads(block) for block in json_blocks]
    print(parsed_blocks)
    return parsed_blocks

def flatten_json_to_text(json_list, parent_key=""):
    """
    Recursively flattens nested JSON objects and formats them into natural-language-like text.
    """
    parts = []
    print(json_list)
    for obj in json_list:
        print(obj)
        if isinstance(obj, dict):
            sub_parts = []
            for key, value in obj.items():
                label = f"{parent_key} {key}".strip()
                if isinstance(value, dict):
                    sub_parts.append(flatten_json_to_text([value], label))
                elif isinstance(value, list):
                    list_items = ", ".join(str(v) for v in value)
                    sub_parts.append(f"{label}: {list_items}")
                else:
                    sub_parts.append(f"{label}: {value}")
            parts.append("; ".join(sub_parts))
        else:
            parts.append(str(obj))

    return ",".join(parts)

def stream_summary(prompt: str, stop_string: str = "=== End of Output ==="):
    """
    Streams output sentence by sentence, stopping immediately after encountering the stop_string.
    """
    print(prompt)
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    attention_mask = tokenizer(prompt, return_tensors="pt")["attention_mask"].to(device)
    
    streamer = TextIteratorStreamer(
        tokenizer, skip_prompt=True, skip_special_tokens=True
    )

    generation_kwargs = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "max_new_tokens": 1000,
        "temperature": 0.0,
        "top_p": 1.0,
        "do_sample": False,
        "num_beams": 1,
        "eos_token_id": tokenizer.eos_token_id,
        "streamer": streamer,
    }

    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    buffer = ""
    temp = ""
    for token in streamer:
        buffer += token
        temp += token
    
        if stop_string in buffer:
            # Only yield up to the stop string, discard the rest
            break
        #yield token
        
        # Only yield if we’re sure the stop string isn’t in progress
        if not stop_string.startswith(temp.strip()):
            yield temp
            temp = ""
        

table_row = [
        ["Empty Cell", "Population", "GDP"],
        ["China", "1.3 bil", "10bil"],
        ["Empty Cell", "Pop1", "Pop2", "GDP"],
        ["US", "500mil", "20mil", "10bil"]
    ]