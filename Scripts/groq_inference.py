"""
import os
from groq import Groq

# Create client
client = Groq(
    # This is the default and can be omitted
    api_key=INSERT_API_KEY)

# Create prompt
bio_prompt = '''Context: I want you to extract semantic triples from the following paragraph.
Rules: The subject of each triple is a chemical. Only use information explicitly present in the paragraph, do not hallucinate. Do not create any fictional or incorrect outputs. Strictly follow all rules and guidelines given. If the object of the triple has more than one noun, split it into separate triples with only one noun each. Do not repeat any triples. The output must be a list of the triples you are most confident in, with each triple in the format [“subject”, “predicate”, “object”].
Q: Extract triples on the part of the human body the chemical subjects can be found in. Use the predicate "biolocation is" for these triples. The object of each triple must be a human body part. If you cannot find any information on this, do not output any triples.
Paragraph: '''
exp_prompt = 'Q: Now, extract triples on the human exposure route of the chemical subjects. Use the predicate "exposed through" for these triples. If you cannot find any information on this, do not output any triples.'
source_prompt = 'Q: Now, extract triples on what food or organism the chemical subject is sourced from. Use the predicate "sourced through" for these triples. If you cannot find any information on this, do not output any triples.'
dis_prompt = 'Q: Now, extract triples on what disease the chemical subject causes. Use the predicate "causes" for these triples. The object of each triple must be a disease. If you cannot find any information on this, do not output any triples.'
inv_prompt = 'Q: Now, extract triples on the biological mechanism the chemical subject is a part of. Use the predicate "involved in" for these triples. If you cannot find any information on this, do not output any triples.'
role_prompt = 'Q: Now, extract triples on the biological role the chemical subject has. Use the predicate "has role of" for these triples. If you cannot find any information on this, do not output any triples.'

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of low latency LLMs",
        }
    ],
    model="mixtral-8x7b-32768",
)
print(chat_completion.choices[0].message.content)
"""

# # Prompt for all questions combined
    # combined_prompt = '''Context: I want you to extract semantic triples from the following paragraph.
    # Rules: The subject of each triple is a chemical. Only use information explicitly present in the paragraph, do not hallucinate. Do not create any fictional or incorrect outputs. Strictly follow all rules and guidelines given. If the object of the triple has more than one noun, split it into separate triples with only one noun each. Do not repeat any triples. The output must be a list of the triples you are most confident in, with each triple in the format [“subject”, “predicate”, “object”].
    # Q: Extract triples on the part of the human body the chemical subjects can be found in. Use the predicate "biolocation is" for these triples. The object of each triple must be a human body part. If you cannot find any information on this, do not output any triples.
    # Q: Now, extract triples on the human exposure route of the chemical subjects. Use the predicate "exposed through" for these triples. If you cannot find any information on this, do not output any triples.
    # Q: Now, extract triples on what food or organism the chemical subject is sourced from. Use the predicate "sourced through" for these triples. If you cannot find any information on this, do not output any triples.
    # Q: Now, extract triples on what disease the chemical subject causes. Use the predicate "causes" for these triples. The object of each triple must be a disease. If you cannot find any information on this, do not output any triples.
    # Q: Now, extract triples on the biological mechanism the chemical subject is a part of. Use the predicate "involved in" for these triples. If you cannot find any information on this, do not output any triples.
    # Q: Now, extract triples on the biological role the chemical subject has. Use the predicate "has role of" for these triples. If you cannot find any information on this, do not output any triples.
    # Paragraph: '''

    # # Store results
    # result = conversation_buf.invoke(combined_prompt + absract)['response']

    # # memory must be cleared after each input
    # conversation_buf.memory.clear()

    # print(result)

import streamlit as st
import os
from groq import Groq
import random
import ast
import re
from tqdm import tqdm
import json

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate


def batch_text_into_segments(text, segment_length=500):
    """
    Batch the text into segments of specified length.
    """
    segments = []
    words = text.split()
    for i in range(0, len(words), segment_length):
        segment = ' '.join(words[i:i+segment_length])
        segments.append(segment)
    return segments

def write_to_jsonl(data, filename):
    """
    Write data to a JSONL file.
    """
    with open(filename, "a", encoding="utf-8") as output_file:
        for line in data:
            output_file.write(json.dumps(line) + "\n")

def main(data_path, output_path):
    # Get Groq API key
    groq_api_key = "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"
    
    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name='mixtral-8x7b-32768',
            temperature=0.1
    )
    # Initialize conversation chain
    conversation_buf = ConversationChain(
        llm=groq_chat,
        memory=ConversationBufferMemory()
    )

    # Prompt for all questions combined
    # combined_prompt = '''Context: I want you to extract semantic triples from the following paragraph.
    # Rules: The subject of each triple is a chemical. Only use information explicitly present in the paragraph, do not hallucinate. Do not create any fictional or incorrect outputs. Strictly follow all rules and guidelines given. If the object of the triple has more than one noun, split it into separate triples with only one noun each. Do not repeat any triples. The output must be a list of the triples you are most confident in, with each triple in the format [“subject”, “predicate”, “object”].
    # Q: Extract triples on the part of the human body the chemical subjects can be found in. Use the predicate "biolocation is" for these triples. The object of each triple must be a human body part. If you cannot find any information on this, do not output any triples.
    # Q: Now, extract triples on the human exposure route of the chemical subjects. Use the predicate "exposed through" for these triples. If you cannot find any information on this, do not output any triples.
    # Q: Now, extract triples on what food or organism the chemical subject is sourced from. Use the predicate "sourced through" for these triples. If you cannot find any information on this, do not output any triples.
    # Q: Now, extract triples on what disease the chemical subject causes. Use the predicate "causes" for these triples. The object of each triple must be a disease. If you cannot find any information on this, do not output any triples.
    # Q: Now, extract triples on the biological mechanism the chemical subject is a part of. Use the predicate "involved in" for these triples. If you cannot find any information on this, do not output any triples.
    # Q: Now, extract triples on the biological role the chemical subject has. Use the predicate "has role of" for these triples. If you cannot find any information on this, do not output any triples.
    # Paragraph: '''
    bio_prompt = '''Context: I want you to extract semantic triples from the following paragraph.
    Rules: The subject of each triple is a chemical. Only use information explicitly present in the paragraph, do not hallucinate. Do not create any fictional or incorrect outputs. Strictly follow all rules and guidelines given. If the object of the triple has more than one noun, split it into separate triples with only one noun each. Do not repeat any triples. The output must be a list of the triples you are most confident in, with each triple in the format [“subject”, “predicate”, “object”].
    Q: Extract triples on the part of the human body the chemical subjects can be found in. Use the predicate "biolocation is" for these triples. The object of each triple must be a human body part. If you cannot find any information on this, do not output any triples.
    Paragraph: '''
    exp_prompt = 'Q: Now, extract triples on the human exposure route of the chemical subjects. Use the predicate "exposed through" for these triples. If you cannot find any information on this, do not output any triples.'
    source_prompt = 'Q: Now, extract triples on what food or organism the chemical subject is sourced from. Use the predicate "sourced through" for these triples. If you cannot find any information on this, do not output any triples.'
    dis_prompt = 'Q: Now, extract triples on what disease the chemical subject causes. Use the predicate "causes" for these triples. The object of each triple must be a disease. If you cannot find any information on this, do not output any triples.'
    inv_prompt = 'Q: Now, extract triples on the biological mechanism the chemical subject is a part of. Use the predicate "involved in" for these triples. If you cannot find any information on this, do not output any triples.'
    role_prompt = 'Q: Now, extract triples on the biological role the chemical subject has. Use the predicate "has role of" for these triples. If you cannot find any information on this, do not output any triples.'

    folder_path = data_path  # Replace with the path to your folder containing text files

    count = 0
    file_count = 0
    for filename in tqdm(os.listdir(folder_path), desc="Processing files"):
        skip = False
        if filename.endswith(".txt"):
            output = []
            id = filename.replace(".txt", "")
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
                text = file.read()
                segments = batch_text_into_segments(text)
                
                for segment in segments:
                    # Check if this is a reference section
                    if "==== Refs" in segment:
                        skip = True
                        continue
                    elif skip:
                        continue

                    # Store results
                    # results = conversation_buf.invoke(combined_prompt + segment)['response']
                    results = []
                    results.append(conversation_buf.invoke(bio_prompt+segment)['response'])
                    results.append(conversation_buf.invoke(exp_prompt)['response'])
                    results.append(conversation_buf.invoke(source_prompt)['response'])
                    results.append(conversation_buf.invoke(dis_prompt)['response'])
                    results.append(conversation_buf.invoke(inv_prompt)['response'])
                    results.append(conversation_buf.invoke(role_prompt)['response'])

                    # memory must be cleared after each input
                    conversation_buf.memory.clear()

                    # Find and append the extracted lists for each prompt
                    # print(results)
                    for result in results:
                        # start_index = result.find("[[")
                        # end_index = result.find("]]") + 2
                        
                        # if start_index != -1 and end_index != -1:
                        #     extracted_list = result[start_index:end_index]
                        #     output.append({"id": filename, "output": extracted_list})
                        print(result)
                        # r'\["[^"]+",\s*"[^"]+",\s*"[^"]+"\]'
                        pattern =  r'\["([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\]'
                        extracted_list = re.findall(pattern, result)
                        if extracted_list != []:
                            output.append({"id": id, "output": extracted_list})

            count += len(output)
            
            # Write output to JSONL files with a maximum of 1000 lines per file
            write_to_jsonl(output, f"{output_path}/output_{str(file_count)}.jsonl")

            # Increment counter
            if count >= 1000:
                count = 0
                file_count += 1


if __name__ == "__main__":
    data_path = "Triplet_Extraction/Test_data"  # Specify the path to your folder containing text files
    output_path = "Triplet_Extraction/Output"
    main(data_path, output_path)
