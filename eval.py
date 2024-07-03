'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-07-01 13:33:16
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-07-03 17:27:20
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/eval.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''

from agents.agent_manager import AgentManager
import json
from sklearn.metrics import accuracy_score, f1_score 
import pdb

manager: AgentManager = AgentManager(config_path='./config.toml')

# Load existing predictions if any
try:
    with open('predictions.json', 'r') as f:
        predictions = json.load(f)
except FileNotFoundError:
    predictions = {}

# PubMedQA data load
with open("datasets/pubmedqa/data/test_set.json", 'r') as f:
    pubmedqa_test_data = json.load(f)

def prepare_input_text(entry):
    question = entry.get("QUESTION", "")
    context = entry.get("CONTEXT", "")
    meshes = ", ".join(entry.get("MESHES", []))
    year = entry.get("YEAR", "")
    
    input_text = f"Question: {question}\nContext: {context}\nMESHES: {meshes}\nYEAR: {year}"
    return input_text

# Generate predictions
for key, values in pubmedqa_test_data.items():
    if key not in predictions:
        input_text = prepare_input_text(values)
        try:
            output = manager.run(input_text=input_text)
            predictions[key] = output
            # Save predictions immediately after each prediction is made
            with open('predictions.json', 'w') as f:
                json.dump(predictions, f, indent=4)
        except Exception as e:
            print(f"Error processing {key}: {e}")

# Load ground truth data
with open('datasets/pubmedqa/data/test_ground_truth.json', 'r') as f:
    ground_truth = json.load(f)

# Evaluate predictions
assert set(ground_truth.keys()) <= set(predictions.keys()), 'All instances in the test set must have been predicted.'

pmids = list(ground_truth.keys())
truth = [ground_truth[pmid] for pmid in pmids]
preds = [predictions.get(pmid) for pmid in pmids]

acc = accuracy_score(truth, preds)
maf = f1_score(truth, preds, average='macro')

print('Accuracy %f' % acc)
print('Macro-F1 %f' % maf)