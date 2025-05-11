import pandas as pd

df = pd.read_csv("results.csv")

average = df.groupby('Course Name')['Total (100)'].mean()
print(average, '\n\n')

pyscho = df[df['Course Name'] == 'Introduction To Cognitive Psychology'].sort_values(by = 'Assignment (25)', ascending=False)
print(pyscho, '\n\n')

other = df[df['Course Name'] != 'Introduction To Cognitive Psychology'].sort_values(by = 'Total (100)', ascending=False)
print(other, '\n\n')

failed = df[(df['Exam (75)'] < 30) | (df['Assignment (25)'] < 10)]
print(failed)
