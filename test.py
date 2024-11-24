import pandas as pd;

CSV_FILE = "results.csv"
df = pd.read_csv(CSV_FILE)

# Group by 'Course Name' and calculate the mean score
average_scores = df.groupby('Course Name')['Final Score (out of 100)'].mean()

# Print the results
print(average_scores)