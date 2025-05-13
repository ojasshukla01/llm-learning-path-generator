import streamlit as st
import pandas as pd
from fpdf import FPDF
import sys
import os
import re

# ✅ Add project root to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.prompt_templates import build_learning_prompt
from models.learning_model import get_learning_plan
from utils.resume_parser import extract_text_from_pdf
from utils.calendar_export import export_learning_plan_to_ics
from utils.prompt_templates import build_gap_analysis_prompt
import unicodedata

def remove_non_ascii(text):
    return ''.join(c for c in text if ord(c) < 128)

# ✅ Setup
st.set_page_config(page_title="Learning Path Generator", layout="centered")
st.title("📚 Personalized Learning Path Generator")

# 📥 Form UI
with st.form("user_form"):
    name = st.text_input("Your Name", "Ojas Shukla")
    goal = st.text_input("Your Goal", "Become a Data Engineer")
    skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])
    style = st.selectbox("Learning Style", ["Video-heavy", "Text-heavy", "Hands-on Projects"])
    hours = st.slider("Hours/week", 2, 30, 10)
    duration = st.slider("Duration (months)", 1, 12, 4)
    resume_file = st.file_uploader("Upload your LinkedIn Resume (.pdf)", type=["pdf"])
    submit = st.form_submit_button("Generate")

if submit:
    # ✅ Create folders
    os.makedirs("output/learning_paths", exist_ok=True)
    os.makedirs("output/learning_paths_csv", exist_ok=True)
    os.makedirs("output/learning_paths_pdf", exist_ok=True)
    os.makedirs("input/resumes", exist_ok=True)
    
    # ✅ Build user dict and generate prompt
    user = {
        "name": name,
        "goal": goal,
        "skill_level": skill_level,
        "preferred_style": style,
        "available_hours_week": hours,
        "duration_months": duration
    }

    # ✅ Parse resume if provided
    linkedin_bio = ""
    if resume_file is not None:
        resume_save_path = f"input/resumes/{name.replace(' ', '_')}_resume.pdf"
        with open(resume_save_path, "wb") as f:
            f.write(resume_file.read())
        linkedin_bio = extract_text_from_pdf(resume_save_path)
        
    # ✅ Gap Analysis
    gap_analysis = ""
    if linkedin_bio:
        gap_prompt = build_gap_analysis_prompt(user, linkedin_bio)
        gap_analysis = get_learning_plan(gap_prompt)


    prompt = build_learning_prompt(user, linkedin_bio)
    output = get_learning_plan(prompt)
    
    # ✅ Display Skill Gap Table
    if gap_analysis:
        st.subheader("🧠 Skill Audit Summary")
        st.markdown("""
        This table summarizes your resume-based skill alignment with your goal, and gives optional career direction if gaps are large:
        """)
        st.markdown(gap_analysis, unsafe_allow_html=True)

    # ✅ File setup
    base_name = f"{name.replace(' ', '_')}_{goal.replace(' ', '_')}"
    txt_path = f"output/learning_paths/{base_name}.txt"
    csv_path = f"output/learning_paths_csv/{base_name}.csv"
    pdf_path = f"output/learning_paths_pdf/{base_name}.pdf"

    # ✅ Save .txt
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(output)

    # ✅ Display full roadmap
    st.subheader("📈 Full Learning Path")
    st.markdown(output)

    # ✅ Parse weeks from output
    st.subheader("📋 Weekly Breakdown (Interactive View)")
    lines = output.split("\n")
    weeks = []
    week = None

    for line in lines:
        line = line.strip()
        if line.lower().startswith("week"):
            if week:
                weeks.append(week)
            week = {"Week": line, "Focus": "", "Resources": "", "Task": ""}
        elif line.lower().startswith("- focus:"):
            week["Focus"] = line.replace("- Focus:", "").strip()
        elif line.lower().startswith("- resources:"):
            week["Resources"] = line.replace("- Resources:", "").strip()
        elif line.startswith("http") or "www." in line:
            if week:
                week["Resources"] += "\n" + line.strip()
        elif line.lower().startswith("- task:"):
            week["Task"] = line.replace("- Task:", "").strip()

    if week:
        weeks.append(week)

    df_weeks = pd.DataFrame(weeks)

    for i, row in df_weeks.iterrows():
        with st.expander(row['Week']):
            st.markdown(f"**Focus:** {row['Focus']}")
            st.markdown(f"**Resources:** {row['Resources']}")
            st.markdown(f"**Task:** {row['Task']}")
            
    # ✅ Skill Gap Analysis
    gap_analysis = ""
    if linkedin_bio:
        gap_prompt = build_gap_analysis_prompt(user, linkedin_bio)
        gap_analysis = get_learning_plan(gap_prompt)
            
    # ✅ Generate .ics calendar file
    ics_path = export_learning_plan_to_ics(df_weeks, name)

    with open(ics_path, "rb") as f:
        st.download_button("📆 Download Calendar (.ics)", f, file_name=os.path.basename(ics_path))

    # ✅ Save CSV
    df_weeks.to_csv(csv_path, index=False)

    # ✅ Save PDF with formatted output
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ✅ Skill Audit Summary – ONE TIME ONLY (before weekly roadmap)
    if gap_analysis:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Skill Audit Summary", ln=True)
    
        # Table header
        pdf.set_font("Arial", "B", 11)
        pdf.cell(50, 10, "Existing Skills", border=1)
        pdf.cell(50, 10, "Skill Gaps", border=1)
        pdf.cell(55, 10, "Recommended Topics", border=1)
        pdf.cell(0, 10, "Career Suggestions", ln=True, border=1)

        # Table rows
        pdf.set_font("Arial", "", 10)
        clean_gap = remove_non_ascii(gap_analysis)

        for line in clean_gap.split("\n"):
            if "|" in line and not line.lower().startswith("existing") and "---" not in line:
                columns = [col.strip() for col in line.split("|")[1:-1]]  # strip outer pipes
                if len(columns) == 4:
                    pdf.cell(50, 10, columns[0][:30], border=1)
                    pdf.cell(50, 10, columns[1][:30], border=1)
                    pdf.cell(55, 10, columns[2][:35], border=1)
                    pdf.cell(0, 10, columns[3][:35], border=1, ln=True)
        pdf.ln(10)

    # ✅ Function to wrap long text blocks for weekly roadmap
    def add_wrapped_text(pdf, label, content, is_link=False):
        pdf.set_font("Arial", "B", 11)
        pdf.cell(30, 10, f"{label}:", ln=False)
        pdf.set_font("Arial", "", 11)

        if is_link:
            urls = re.findall(r'(https?://\S+)', content)
            for url in urls:
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 10, url, ln=True, link=url)
                pdf.set_text_color(0, 0, 0)
        else:
            pdf.multi_cell(0, 10, content)
        pdf.ln(2)

    # ✅ Weekly roadmap section
    for _, row in df_weeks.iterrows():
        # 📌 Week Header
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, row["Week"], ln=True)

        add_wrapped_text(pdf, "Focus", row["Focus"])
        add_wrapped_text(pdf, "Resources", row["Resources"], is_link=True)
        add_wrapped_text(pdf, "Task", row["Task"])

        pdf.ln(5)

    # ✅ Save final PDF
    pdf.output(pdf_path)

    # ✅ Download Buttons (aligned)
    st.subheader("⬇️ Download Your Plan")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button("📄 TXT File", output, file_name=f"{base_name}.txt")

    with col2:
        with open(csv_path, "rb") as f:
            st.download_button("📊 CSV File", f, file_name=f"{base_name}.csv")

    with col3:
        with open(pdf_path, "rb") as f:
            st.download_button("🧾 PDF File", f, file_name=f"{base_name}.pdf")
