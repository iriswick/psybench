import json
import os
from dotenv import load_dotenv

# This imports the class from your OTHER file (judge.py)
from judge import PsyJudge 

# 1. Load the API Key safely
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 2. Initialize the Judge
# We pass the key we just loaded into the class constructor
judge = PsyJudge(api_key)

# Load experiments from the external file instead of hardcoding
with open("data.json", "r") as f:
    my_experiments = json.load(f)

results = []
print(f"Loaded {len(my_experiments)} experiments. Starting analysis...")

# ... rest of the loop code ...
# 4. Run the Analysis Loop
results = []

print("Starting analysis...")

for exp in my_experiments:
    print(f"Analyzing scenario: {exp['id']}...")
    
    # Call the judge
    score = judge.evaluate_response(
        history=exp['history'], 
        model_response=exp['final_response'],
        harm_type=exp['harm_type']
    )
    
    # Store the result
    # We combine the original ID with the new scores
    final_record = {
        "id": exp['id'],
        "scores": score
    }
    results.append(final_record)
    print(f" -> Scored! DCS: {score.get('DCS')}")

# 5. Save results to a file
with open("final_grades.json", "w") as f:
    json.dump(results, f, indent=2)


print("Done! Results saved to final_grades.json")
