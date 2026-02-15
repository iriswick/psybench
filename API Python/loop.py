import json
import os
from dotenv import load_dotenv
from judge import PsyJudge 

# 1. Load the API Key safely
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 2. Initialize the Judge
if not api_key:
    print("Error: API Key not found! Check your .env file.")
    exit()

judge = PsyJudge(api_key)

# 3. Load experiments from the external file
print("Loading data.json...")
try:
    with open("data.json", "r") as f:
        my_experiments = json.load(f)
    print(f"Successfully loaded {len(my_experiments)} experiments.")
except FileNotFoundError:
    print("Error: Could not find 'data.json'. Make sure it exists in the same folder!")
    exit()

# 4. Run the Analysis Loop
results = []
print("Starting analysis now...")

for exp in my_experiments:
    print(f"Analyzing scenario: {exp['id']}...")
    
    # Call the judge
    try:
        score = judge.evaluate_response(
            history=exp['history'], 
            model_response=exp['final_response'],
            harm_type=exp['harm_type']
        )
        
        # Store the result
        final_record = {
            "id": exp['id'],
            "scores": score
        }
        results.append(final_record)
        print(f" -> Scored! DCS: {score.get('DCS')}")
        
    except Exception as e:
        print(f" -> Failed to score {exp['id']}: {e}")

# 5. Save results to a file
with open("final_grades.json", "w") as f:
    json.dump(results, f, indent=2)

print("Done! Results saved to final_grades.json")
