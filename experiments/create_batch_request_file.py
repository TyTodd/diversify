import json

prompt_template = "You are a {race} {gender} writing a personal statement for your college applications. First think of experiences a {race} {gender} might run into in college. Really use your imagination for this. Then write a 600 word personal statement about that experience."
num_samples = 300
black_percentage = .05
hispanic_percentage = .1
asian_percentage = .47
indigenous_percentage = .01
white_percentage = .37

assert black_percentage + hispanic_percentage + asian_percentage + indigenous_percentage + white_percentage == 1

def generate_prompts(race, gender, count):
    prompts = []
    for i in range(count):
        formatted_prompt = prompt_template.format(race=race, gender=gender)
        prompts.append(formatted_prompt)
    return prompts

# Generate prompts for each race and gender
prompts = []
prompts.extend(generate_prompts("black", "female", int(black_percentage * num_samples) // 2))
prompts.extend(generate_prompts("black", "male", int(black_percentage * num_samples) // 2))
prompts.extend(generate_prompts("hispanic", "female", int(hispanic_percentage * num_samples) // 2))
prompts.extend(generate_prompts("hispanic", "male", int(hispanic_percentage * num_samples) // 2))
prompts.extend(generate_prompts("asian", "female", int(asian_percentage * num_samples) // 2))
prompts.extend(generate_prompts("asian", "male", int(asian_percentage * num_samples) // 2))
prompts.extend(generate_prompts("indigenous", "female", int(indigenous_percentage * num_samples) // 2))
prompts.extend(generate_prompts("indigenous", "male", int(indigenous_percentage * num_samples) // 2))
prompts.extend(generate_prompts("white", "female", int(white_percentage * num_samples) // 2))
prompts.extend(generate_prompts("white", "male", int(white_percentage * num_samples) // 2))

# Write prompts to JSONL file
with open("batch_requests.jsonl", "w") as f:
    for i, prompt in enumerate(prompts):
        request = {
            "custom_id": f"request-{i+1}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000
            }
        }
        json.dump(request, f)
        f.write("\n")

print(f"Generated {len(prompts)} prompts and saved them to batch_requests.jsonl")

