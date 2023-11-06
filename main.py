import importlib
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

# if __name__ == "__main__":
#     # Fetch data from Rainforest API
#     try:
#         cmd = ["python3", "examples/rainforest/data_ingestion_cron_job.py"]

#         subprocess.run(cmd, check=True)
#     except subprocess.CalledProcessError:
#         print("Script execution failed.")
#     except FileNotFoundError:
#         print("Python interpreter or the script was not found.")

#     # Run Discounts API
#     host = os.environ.get("HOST", "0.0.0.0")
#     port = int(os.environ.get("PORT", 8080))
#     app_api = importlib.import_module("examples.api.app")
#     app_api.run(host=host, port=port)
import json
import os

outer_dir = "examples"
data_dir = "rainforest"

full_data_dir = os.path.join(outer_dir, data_dir)

def load_data():

  jsonl_files = [f for f in os.listdir(full_data_dir) if f.endswith(".jsonl")]

  data = []

  for f in jsonl_files:
    file_path = os.path.join(full_data_dir, f)
    with open(file_path) as jsonl:
      for line in jsonl:
        data.append(json.loads(line))

  return data

if __name__ == "__main__":
  all_data = load_data()
host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 8080))
app_api = importlib.import_module("examples.api.app")
app_api.run(host=host, port=port)

  # Rest of code...
  
  # Rest of code to process and run app