import json

# Load the original JSONL file
with open('Data/train_data.jsonl', 'r', encoding="utf-8") as f:
    data = [json.loads(line) for line in f]

# Define the system prompt
system_prompt = "The task is to extract biology-related triples from scientific research papers. The rules are:\n1. Only use the following predicates in the triple: “causes”, ”biolocation is”, “exposed through”, “sourced through”, “has role of”, “involved in”.\n2. If there is more than one noun in the object, separate it into multiple triples.\n3. If you don't find relevant biology-related triples in the paper or you are not sure, return: null."

# Initialize the new data list
new_data = []

# Process each item in the original data
for item in data:
    # Extract input and output
    user_message = item["input"] + "\nA: "
    response = item["output"]

    # Append the formatted data to the new data list
    new_data.append({
        "inputs": f"<s>[INST] <<SYS>>\n{{ {system_prompt} }}\n<</SYS>>\n\n{{ {user_message} }} [/INST] {response} </s>"
    })

# Write the new JSONL file
with open('Data/Gradient_AI_train_data.jsonl', 'w') as f:
    for item in new_data:
        json.dump(item, f)
        f.write('\n')
