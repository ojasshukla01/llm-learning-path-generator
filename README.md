# 🤖 LLM-Powered Personalized Learning Path Generator

This project is an end-to-end, open-source AI-powered app that generates personalized learning roadmaps using LLMs. Users can upload their resume (LinkedIn PDF), specify their goals (e.g., "Become a Data Engineer"), and instantly receive:
- A skill gap audit in table form
- A weekly learning plan
- Calendar export (.ics)
- Downloadable outputs: `.txt`, `.csv`, `.pdf`

## 🚀 Features

- ✅ Upload resume to extract current skills
- ✅ Identify key skill gaps for the user’s goal
- ✅ Generate recommended learning topics
- ✅ Create a weekly, goal-aligned roadmap
- ✅ Export to PDF, CSV, TXT, and iCal (.ics)
- ✅ Fully freeware: Streamlit, LangChain/OpenRouter, Faker, DuckDB, etc.

## 🧠 Example Use Case

**Goal:** Become a Data Engineer in 4 months  
**Resume:** Includes Python, Excel, basic SQL  
→ Output: Skill Audit Table + 16-week roadmap with hands-on tasks

## 📦 Tech Stack

- Python, Streamlit
- LangChain/OpenRouter API (Free-tier compatible)
- PDF Parsing with PyMuPDF
- FPDF for clean export
- Pandas for tabular breakdowns
- ICS library for calendar generation

## 📁 Folder Structure

```
├── app/
│   └── streamlit_app.py         # Main Streamlit UI
├── utils/
│   ├── prompt_templates.py      # Prompt builders
│   ├── resume_parser.py         # PDF to text
│   └── calendar_export.py       # .ics export
├── output/
│   ├── learning_paths/          # .txt
│   ├── learning_paths_csv/      # .csv
│   ├── learning_paths_pdf/      # .pdf
│   └── calendar/                # .ics
├── input/resumes/               # Uploaded resumes
```

## 🔧 Setup Instructions

1. Clone the repo  
2. Create `.env` and add your OpenRouter or OpenAI API key  
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app/streamlit_app.py
```

## 🌐 API Key (.env Example)
```
OPENAI_API_KEY=your-key-here
```

## 📜 License

MIT — Free to use with credit

---

Built by Ojas Shukla ✨
GitHub: [ojasshukla01](https://github.com/ojasshukla01)