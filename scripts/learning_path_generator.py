import pandas as pd

import sys
import os

# ✅ Add project root to sys.path so we can import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.validator import validate_user_data
from utils.prompt_templates import build_learning_prompt
from models.learning_model import get_learning_plan

# ✅ Load user data
df = validate_user_data("data/simulated_users.csv")

# ✅ Create output folder if not exists
os.makedirs("output/learning_paths", exist_ok=True)

for i, user in df.iterrows():
    prompt = build_learning_prompt(user)
    try:
        plan = get_learning_plan(prompt)
        filename = f"{user['name'].replace(' ', '_')}_{user['goal'].replace(' ', '_')}.txt"
        path = os.path.join("output/learning_paths", filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(plan)
        print(f"✅ Saved: {filename}")
    except Exception as e:
        print(f"❌ Failed for {user['name']}: {e}")
