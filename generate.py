from transformers import AutoTokenizer, AutoModelForCausalLM

model_name_or_path = "williamsl/DungeonsAndDragonsGPT" #path/to/your/model/or/name/on/hub
device = "cpu" # or "cuda" if you have a GPU

model = AutoModelForCausalLM.from_pretrained(model_name_or_path).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

inputs = tokenizer.encode("This movie was really", return_tensors="pt").to(device)
outputs = model.generate(inputs)
print(tokenizer.decode(outputs[0]))