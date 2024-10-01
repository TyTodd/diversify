import json
from openai import OpenAI
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Access the API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Ensure the API key is set
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")
client = OpenAI(api_key=OPENAI_API_KEY)

prompt_template = "You are a {race} {gender} writing a personal statement for your college applications. First think of experiences a {race} {gender} might run into in college. Really use your imagination for this. Then write a 600 word personal statement about that experience."
races = ["hispanic", "black", "indigenous", "asian", "white"]
genders = ["female", "male"]
# Load batch_requests.jsonl
with open('batch_requests.jsonl', 'r') as file1:
    batch_requests = [json.loads(line1) for line1 in file1]
    print("batch_requests",len(batch_requests))
    # Load batch_output.jsonl
    with open('batch_output.jsonl', 'r') as file2:
        batch_output = [json.loads(line2) for line2 in file2]
        
        essays = []
        for i, request in enumerate(batch_requests):
            prompt = request['body']["messages"][1]["content"]
            for r_index,race in enumerate(races):
                    for g_index, gender in enumerate(genders):
                        if f"{race} {gender}" in prompt:
                            row = []
                            response = batch_output[i]["response"]["body"]["choices"][0]["message"]["content"]
                            embedding = client.embeddings.create(input=response, model="text-embedding-3-small", dimensions=256).data[0].embedding
                            embedding = np.array(embedding)
                            row.append(embedding)
                            row.append(np.array([r_index,g_index]))
                            essays.append(row)
import pickle

# Convert essays list to a numpy array
# essays_array = np.array(essays, dtype=object)

db = pd.DataFrame(essays)
db.to_pickle('synthetic_dataset.pkl')

print(f"Saved {len(essays)} essays to synthetic_dataset.pkl")
# print("essays",essays)


