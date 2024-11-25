import pandas as pd;

CSV_FILE = "results.csv"
df = pd.read_csv(CSV_FILE)

average_scores = df.groupby('Course Name')['Marks'].mean()
print(average_scores)

# Group by 'Course Name' and calculate the mean score
a = df.loc[df["Course Name"] == "Conservation Geography"]

a = a.sort_values(by = "Marks", ascending=False)

# Print the results
print(a)