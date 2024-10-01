import json
import os

# Create the synthetic-data folder
os.makedirs("synthetic-data", exist_ok=True)

# Read the batch_output.jsonl file
with open("experiments/batch_output.jsonl", "r") as jsonl_file:
    for i, line in enumerate(jsonl_file):
        # Parse each JSON line
        data = json.loads(line)
        
        # Create a file for each student
        filename = f"synthetic-data/student{i+1}.txt"
        with open(filename, "w") as student_file:
            # Write the JSON data to the file
            # You can customize this part to write specific fields or format the data as needed
            content = data["response"]["body"]["choices"][0]["message"]["content"]
            student_file.write(content)
print("Synthetic data files have been created.")
