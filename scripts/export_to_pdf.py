import os
from fpdf import FPDF

input_folder = "output/learning_paths"
output_folder = "output/learning_paths_pdf"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        path = os.path.join(input_folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in content.split("\n"):
            pdf.multi_cell(0, 10, line)

        pdf_name = filename.replace(".txt", ".pdf")
        pdf.output(os.path.join(output_folder, pdf_name))
        print(f"✅ PDF exported: {pdf_name}")
