from peft import AutoPeftModelForCausalLM, PeftModel
from transformers import AutoModelForCausalLM
import torch
import os

model_id = "Open_Orca_Weights"

model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, load_in_8bit=False,
                                             device_map="auto",
                                             trust_remote_code=True,
                                             offload_folder="Open_Orca_Weights")

model_path = "Open_Orca_Checkpoints" #"/content/tinyllama/checkpoint-250"

print("Loading Peft")
peft_model = PeftModel.from_pretrained(model, model_path, from_transformers=True, device_map="auto")

model = peft_model.merge_and_unload()