import json
import os
from dotenv import load_dotenv
from judge import PsyJudge 

# 1. Load the API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: API Key not found! Check your .env file.")
    exit()

judge = PsyJudge(api_key)

# 2. Load the Experiments
print("Loading data.json...")
try:
    with open("data.json", "r") as f:
        my_experiments = json.load(f)
    print(f"Successfully loaded {len(my_experiments)} experiments.")
except FileNotFoundError:
    print("Error: Could not find 'data.json'.")
    exit()

# 3. Run Analysis
results = []
print("Starting analysis...")

for exp in my_experiments:
    # Print progress so you know it's working
    print(f"Analyzing {exp['id']}...")
    
    # --- SMART PARSING LOGIC ---
    # We extract the conversation from the "prompts" list
    raw_prompts = exp['prompts']
    
    if not raw_prompts:
        print(f" -> Skipping {exp['id']}: No prompts found.")
        continue

    # 1. The message to grade is the very last one in the list
    final_response_text = raw_prompts[-1] 
    
    # 2. The history is everything BEFORE the last one, joined by newlines
    history_text = "\n".join(raw_prompts[:-1])
    # -----------------------------

    try:
        # BLIND EVALUATION:
        # We DO NOT pass 'archetype' or 'platform' to the judge.
        score = judge.evaluate_response(
            history=history_text, 
            model_response=final_response_text,
            harm_type=exp['harm_type']
        )
        
        # SAVE EVERYTHING:
        # We combine your original metadata with the new scores
        final_record = {
            "id": exp['id'],
            "name": exp.get('name'),
            "theme": exp.get('theme'),
            "condition": exp.get('condition'),
            "harm_type": exp.get('harm_type'),
            "platform": exp.get('platform'),   # Your custom field
            "archetype": exp.get('archetype'), # Your custom field
            "scores": score
        }
        results.append(final_record)
        print(f" -> Scored! DCS: {score.get('DCS')}")
        
    except Exception as e:
        print(f" -> Failed: {e}")

# 4. Save Final Results
with open("final_grades.json", "w") as f:
    json.dump(results, f, indent=2)

print("Done! Results saved to final_grades.json")
