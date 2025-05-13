from ics import Calendar, Event
from datetime import datetime, timedelta
import os

def export_learning_plan_to_ics(weeks_df, user_name, start_date=None):
    cal = Calendar()
    today = datetime.today()
    start_date = start_date or today

    for i, row in weeks_df.iterrows():
        week_start = start_date + timedelta(weeks=i)
        event = Event()
        event.name = f"{row['Week']}: {row['Focus']}"
        event.begin = week_start
        event.duration = timedelta(days=1)
        event.description = f"Resources:\n{row['Resources']}\n\nTask:\n{row['Task']}"
        cal.events.add(event)

    file_name = f"{user_name.replace(' ', '_')}_learning_plan.ics"
    path = f"output/calendar/{file_name}"

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(cal.serialize_iter())
    
    return path
