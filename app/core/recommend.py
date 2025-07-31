import json
import pathlib

ProjectRoot = pathlib.Path(__file__).parent.parent.parent

def load_json(file:str):
    with open(file, 'r', encoding='utf-8') as f:
        recommend_data = json.load(f)
    return recommend_data

recommend_data = load_json(f"{ProjectRoot}/recommendation.json")