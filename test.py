import pandas as pd

df = pd.read_csv("results.csv")

average = df.groupby('Course Name')['Total (100)'].mean()
print(average, '\n\n')

geo = df[df['Course Name'] == 'Conservation Geography'].sort_values(by = 'Total (100)', ascending=False)
print(geo, '\n\n')

cyber = df[df['Course Name'] == 'Cyber Security and Privacy'].sort_values(by = 'Total (100)', ascending=False)
print(cyber, '\n\n')

java = df[df['Course Name'] == 'Programming in Java'].sort_values(by = 'Total (100)', ascending=False)
print(java, '\n\n')

other = df[(df['Course Name'] != 'Cyber Security and Privacy') & (df['Course Name'] != 'Conservation Geography') & (df['Course Name'] != 'Programming in Java')]
other = other.sort_values(by = 'Total (100)', ascending=False)
print(other, '\n\n')

failed = df[(df['Exam (75)'] < 30) | (df['Assignment (25)'] < 10)]
print(failed)
