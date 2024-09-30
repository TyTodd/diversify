import json
import codecs
import re
import os
from flask import Flask, request, jsonify
import zipfile
import shutil

# Path to the directory containing the folders
directory_path = 'data/your_instagram_activity/messages/inbox'
output_path = 'ty_ig_data.jsonl'
# List to store the folder names
def decode_utf8_string(s):
    return s.encode('latin1').decode('utf-8')

def replace_escape_sequences_v3(data):
    if isinstance(data, str):
        return decode_utf8_string(data)
    elif isinstance(data, list):
        return [replace_escape_sequences_v3(item) for item in data]
    elif isinstance(data, dict):
        return {key: replace_escape_sequences_v3(value) for key, value in data.items()}
    else:
        return data

def process(zip_path, app):
    """
    Makes the subject (you) the asssistant and all the people you talk to the user
    """
    # Create a unique directory to extract files (to avoid conflicts)
    extract_path = os.path.join(app.config['EXTRACT_FOLDER'])
    os.makedirs(extract_path, exist_ok=True)
    print(extract_path)
    print(zip_path)

    # Open the ZIP file for reading
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        print(os.path.join(app.config['EXTRACT_FOLDER'], os.path.basename(zip_path).split('.')[0]), "exctractallpath")
        # List to store information about processed files
        files = []

        # Iterate over each file in the ZIP
        for file_info in zip_ref.infolist():
            # if i == 0: 
            #     continue
            file_path = os.path.join(extract_path, file_info.filename)
            
            if "__MACOSX" in file_path:
                continue
            print(file_path)
            if file_info.filename.lower().endswith('.txt'):
                with open(file_path, 'r') as txt:
                    content = txt.read()
                    files.append((os.path.splitext(file_info.filename)[0].split('/')[1], content))
                    
            #         print(file_path)
            #         json_data = json.load(json_file)
            #         print(json_data)
            #         processed_data = replace_escape_sequences_v3(json_data)
            #         if 'participants' not in processed_data or len(processed_data['participants']) != 2:
            #             continue
            #         subject_name = processed_data['participants'][1]['name']
            #         messages = []
            #         for message in processed_data['messages']:
            #             if message['sender_name'] == subject_name and 'content' in message:
            #                 if message['content'] == "Liked a message":
            #                     continue
            #                 messages.append({
            #                     "role": "assistant",
            #                     "content": message['content'],
            #                 })
            #             elif 'content' in message:
            #                 messages.append({
            #                     "role": "user",
            #                     "content": message['content'],
            #                 })
            #         messages = messages[::-1]
            #         messages.insert(0, {"role": "system", "content": f"Your name is {subject_name} and you are having a casual conversation with your friend."})
            #         if len(messages) > 2048:
            #             messages = messages[-2048:]
            #         if not any(message.get("role", None) == "assistant" for message in messages):
            #             continue
            #         while messages[-1]["role"] != "assistant":
            #             messages.pop()
                    
            #         # if len(messages) > 2048: print(folder_name, len(messages))
            #         chats.append({
            #             "messages": messages, # reverse the messages
            #         })

        # Optionally, delete the extracted files after processing
        shutil.rmtree(extract_path)  # This will remove the entire extracted folder

        return files