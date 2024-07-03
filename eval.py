'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-07-01 13:33:16
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-07-02 15:29:09
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/eval.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''

from agents.agent_manager import AgentManager
import json
from sklearn.metrics import accuracy_score, f1_score 
import pdb

manager: AgentManager = AgentManager(config_path='./config.toml')

# PubMedQA data load
with open("datasets/pubmedqa/data/test_set.json", 'r') as f:
    pubmedsq_test_data = json.load(f)

# Define a function to prepare input text for the agent
def prepare_input_text(entry):
    question = entry.get("QUESTION", "")
    context = entry.get("CONTEXT", "")
    meshes = ", ".join(entry.get("MESHES", []))
    year = entry.get("YEAR", "")
    
    # You can choose to include or exclude the year based on your needs
    input_text = f"Question: {question}\nContext: {context}\nMESHES: {meshes}\nYEAR: {year}"
    return input_text

# Generate predictions
predictions = {}
for entry in pubmedsq_test_data:
    pmid = entry["PMID"]
    input_text = prepare_input_text(entry)
    output = manager.run(input_text=input_text)
    predictions[pmid] = output

# Save predictions to a file
with open('predictions.json', 'w') as f:
    json.dump(predictions, f, indent=4)

# Load ground truth data
with open('data/test_ground_truth.json', 'r') as f:
    ground_truth = json.load(f)

# Evaluate predictions
assert set(ground_truth.keys()) == set(predictions.keys()), 'Please predict all and only the instances in the test set.'

pmids = list(ground_truth.keys())
truth = [ground_truth[pmid] for pmid in pmids]
preds = [predictions[pmid] for pmid in pmids]

acc = accuracy_score(truth, preds)
maf = f1_score(truth, preds, average='macro')

print('Accuracy %f' % acc)
print('Macro-F1 %f' % maf)