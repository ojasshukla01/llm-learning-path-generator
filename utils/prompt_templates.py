def build_learning_prompt(user, linkedin_bio=None):
    base_prompt = f"""
You are a highly experienced learning path architect specializing in career upskilling.

🧠 User Profile:
- Goal: "{user['goal']}"
- Current Skill Level: {user['skill_level']}
- Preferred Learning Style: {user['preferred_style']}
- Time Commitment: {user['available_hours_week']} hours/week
- Deadline: {user['duration_months']} months from today
"""

    if linkedin_bio:
        base_prompt += f"\n📄 Additional Background Info (from resume):\n{linkedin_bio}\n"

    base_prompt += """
🧭 Instructions:
1. Break the roadmap into weekly modules for {duration} months.
2. Gradually increase complexity, starting with the fundamentals.
3. For each week, include:
   - 📘 Learning Focus
   - 📌 Suggested Resources (free only)
   - 🎯 Practical Task
4. Avoid repeated resources.
5. Prioritize active learning.
6. Avoid placeholder names like "Google Cloud course" — always include **actual titles and links**

📝 Format:
Week 1:
- Focus: <...>
- Resources:
  - https://youtube.com/xyz
  - https://cloud.google.com/training/gcp-course
- Task: <...>
"""
    return base_prompt


def build_gap_analysis_prompt(user, resume_text):
    return f"""
You are a senior technical mentor and career advisor.

📄 Resume:
{resume_text}

🎯 Goal: "{user['goal']}"

🧠 Instructions:
1. Extract relevant skills already present in the resume.
2. Identify the most critical skill gaps.
3. Recommend learning topics or tools based on these gaps can be multiple if required.
4. Suggest alternate or adjacent roles if the gap is significant (but not mandatory).
5. Output a structured 4-column markdown table.
6. Everything should be as per market trend so do some on going and latest market research as well

📋 Format:
| ✅ Existing Skills | 🚫 Skill Gaps | 📘 Recommended Topics | 💼 Career Suggestions |
|-------------------|---------------|------------------------|------------------------|
| Python            | GCP           | GCP Data Training      | Data Analyst,..,..           |
| Excel             | Airflow       | Airflow DAGs           | BI Analyst,..,..             |
| ...               | ...           | ...                    | ...,..,..                    |

Only return the markdown table. Do not explain anything outside the table.
"""
