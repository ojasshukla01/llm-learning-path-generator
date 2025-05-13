import os
import pandas as pd

input_folder = "output/learning_paths"
output_folder = "output/learning_paths_csv"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        path = os.path.join(input_folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        weeks = []
        for line in lines:
            line = line.strip()
            if line.lower().startswith("week"):
                current_week = line
                weeks.append({"Week": current_week, "Topic": ""})
            elif line:
                if weeks:
                    weeks[-1]["Topic"] += line + " "

        df = pd.DataFrame(weeks)
        csv_name = filename.replace(".txt", ".csv")
        df.to_csv(os.path.join(output_folder, csv_name), index=False)
        print(f"✅ Exported: {csv_name}")
