import pandas as pd

def validate_user_data(path):
    df = pd.read_csv(path)
    df.drop_duplicates(inplace=True)
    required_cols = {'goal', 'skill_level', 'preferred_style', 'available_hours_week', 'duration_months'}
    if not required_cols.issubset(df.columns):
        raise ValueError("Missing required user columns.")
    return df
