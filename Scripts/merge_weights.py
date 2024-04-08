from peft import AutoPeftModelForCausalLM, PeftModel
from transformers import AutoModelForCausalLM
import torch
import os
from transformers import GenerationConfig, AutoTokenizer, BitsAndBytesConfig
from time import perf_counter

model_id ="Open_Orca_Weights"
tokenizer = AutoTokenizer.from_pretrained(model_id)

def formatted_prompt(question)-> str:
    return f"### Human: {question} ### Assistant:"

def generate_response(user_input):

    prompt = formatted_prompt(user_input)
    print("Generating")

    inputs = tokenizer([prompt], return_tensors="pt")
    generation_config = GenerationConfig(penalty_alpha=0.5,do_sample = True,
        top_k=1,temperature=0.1,repetition_penalty=1.2,
        max_new_tokens=500,pad_token_id=tokenizer.eos_token_id
    )
    start_time = perf_counter()

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(**inputs, generation_config=generation_config)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
    output_time = perf_counter() - start_time
    print(f"Time taken for inference: {round(output_time,2)} seconds")

model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32, load_in_8bit=False)
output_2 = generate_response(user_input='Is TMEM106B amyloidogenic protein?')
print("Original")
print(output_2)
                                             
model_path = "Open_Orca_Checkpoints" #"/content/tinyllama/checkpoint-250"
peft_model = PeftModel.from_pretrained(model, model_path, from_transformers=True, device_map="auto")
model = peft_model.merge_and_unload(model)



output = generate_response(user_input='Is TMEM106B amyloidogenic protein?')
print("Fine-tuned")
print(output)