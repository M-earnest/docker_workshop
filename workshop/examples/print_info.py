import pandas as pd
from datetime import datetime


# Create dummy data for EEG subjects demographics
data = {
    'SubjectID': [1, 2, 3, 4, 5],
    'Age': [28, 34, 29, 32, 31],
    'Handedness': ['L', 'R', 'R', 'R', 'L']
}
df = pd.DataFrame(data)

# Save the dataframe to a CSV file
csv_filename = 'demographics.csv'
df.to_csv(csv_filename, index=False)

# Placeholder for the study title
study_title = "Your Study Title Here"

print(f"Date: {datetime.now().strftime('%Y-%m-%d')}\nWelcome to the Docker image for {study_title}. You'll find all relevant information in the README file located in this folder.")
