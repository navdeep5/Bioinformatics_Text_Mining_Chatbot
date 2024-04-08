# @title Select Large Language Model
selected_llm = 'Mistral-7B-OpenOrca' # @param ["Mistral-7B", "Mistral-7B-OpenOrca", "Llama-2-13B-Chat","TinyLlama-1.1B-Chat"]

model_dic = {"Mistral-7B":{"HF_REPO_NAME":"TheBloke/Mistral-7B-Instruct-v0.1-GGUF","HF_MODEL_NAME":"mistral-7b-instruct-v0.1.Q4_K_M.gguf"},
           "Mistral-7B-OpenOrca":{"HF_REPO_NAME":"TheBloke/Mistral-7B-OpenOrca-GGUF","HF_MODEL_NAME":"mistral-7b-openorca.Q5_K_M.gguf"},
             "Llama-2-13B-Chat":{"HF_REPO_NAME":"TheBloke/Llama-2-13B-chat-GGUF","HF_MODEL_NAME":"llama-2-13b-chat.Q4_K_S.gguf"},
             "TinyLlama-1.1B-Chat":{"HF_REPO_NAME":"TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF", "HF_MODEL_NAME":"tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"}
            }

from llama_cpp import Llama

llm = Llama(
    model_path="BioOrca",
    # lora_path="BioOrca",
    n_threads=2, # CPU cores
    n_batch=512, # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
    n_gpu_layers=30, # The max for this model is 30 in a T4, If you use llama 2 70B, you'll need to put fewer layers on the GPU
    n_ctx=4096, # Context window
)