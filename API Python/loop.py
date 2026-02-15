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

# 2. Load the 144 Experiments
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
    print(f"Analyzing {exp['id']} ({exp['archetype']} on {exp['platform']})...")
    
    try:
        # The Judge evaluates the TEXT, not the archetype tag (to keep it unbiased)
        score = judge.evaluate_response(
            history=exp['history'], 
            model_response=exp['final_response'],
            harm_type=exp['harm_type']
        )
        
        # WE SAVE EVERYTHING HERE
        # This is the part that was missing before
        final_record = {
            "id": exp['id'],
            "platform": exp.get('platform'),   # Saves "Character.ai"
            "archetype": exp.get('archetype'), # Saves "The Enabler"
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
