import pandas as pd

RESULT_FILE = "Results-Sem-6.csv"

df = pd.read_csv(RESULT_FILE)

average = df.groupby('Course Name')['Total (100)'].mean()
print(average, '\n\n')

pyscho = df[df['Course Name'] == 'Introduction To Cognitive Psychology'].sort_values(by = 'Total (100)', ascending=False)
print(pyscho, '\n\n')

iiot = df[df['Course Name'] == 'Introduction To Internet Of Things'].sort_values(by = 'Total (100)', ascending=False)
print(iiot, '\n\n')

ebsns = df[df['Course Name'] == 'E-Business'].sort_values(by = 'Total (100)', ascending=False)
print(ebsns, '\n\n')

other = df[(df['Course Name'] != 'Introduction To Internet Of Things') & (df['Course Name'] != 'Introduction To Cognitive Psychology') & (df['Course Name'] != 'E-Business')].sort_values(by = 'Total (100)', ascending=False)
print(other, '\n\n')

failed = df[(df['Exam (75)'] < 30) | (df['Assignment (25)'] < 10)]
print(failed)
