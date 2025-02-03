import json
import pandas as pd
from datetime import datetime

def flatten_json(nested_json):
  flat_data = {}

  def flatten(obj, key=''):
      if isinstance(obj, dict):
          for k, v in obj.items():
              new_key = f"{key}.{k}" if key else k
              flatten(v, new_key)
      elif isinstance(obj, list):
          flat_data[key] = json.dumps(obj)
      else:
          flat_data[key] = obj

  flatten(nested_json)

  for k, v in list(flat_data.items()):
      if isinstance(v, (int, float)) and 'date' in k.lower():
          try:
              flat_data[k] = datetime.utcfromtimestamp(v / 1000).strftime('%Y-%m-%d %H:%M:%S')
          except ValueError:
              pass

  return flat_data

def load_json_file(file_path):
  data = []
  with open(file_path, 'r', encoding='utf-8') as file:
      for line in file:
          try:
              data.append(json.loads(line.strip()))
          except json.JSONDecodeError:
              print("Skipping invalid JSON line")
  return data

file_path = "receipts.json"
data = load_json_file(file_path)
flattened_data = [flatten_json(record) for record in data]

df = pd.DataFrame(flattened_data)
df.to_csv("Receipts_beta.csv", index=False)
