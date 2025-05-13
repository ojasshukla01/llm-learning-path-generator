from faker import Faker
import pandas as pd

fake = Faker()
goals = ['Become a Data Engineer', 'Master NLP', 'Learn Web Development', 'Become an ML Researcher']
levels = ['Beginner', 'Intermediate', 'Advanced']
prefs = ['Video-heavy', 'Text-heavy', 'Hands-on Projects']

users = []
for _ in range(500):
    users.append({
        "name": fake.name(),
        "email": fake.email(),
        "goal": fake.random_element(goals),
        "skill_level": fake.random_element(levels),
        "preferred_style": fake.random_element(prefs),
        "available_hours_week": fake.random_int(min=4, max=20),
        "duration_months": fake.random_int(min=2, max=6)
    })

df = pd.DataFrame(users)
df.to_csv("data/simulated_users.csv", index=False)
print("✅ User data saved to data/simulated_users.csv")