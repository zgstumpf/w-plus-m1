import matplotlib.pyplot as plt

import os
import csv
import glob


csvFiles = [os.path.basename(file) for file in glob.glob("data/*.csv")]
"""
A list of filenames of files that are in the data directory and end in .csv.
"""

HORIZONTAL_LINE = '-' * 40

print('Data files:')
print(HORIZONTAL_LINE)
for filename in csvFiles:
    print(filename)
print(HORIZONTAL_LINE)

file = input("Enter the filename you want to analyze: ").strip()
if file not in csvFiles:
    raise FileNotFoundError(f"{file}")


# Collect data from CSV file
x = []
y = []
with open(os.path.join('data', file), 'r') as csvFile:
    reader = csv.reader(csvFile)
    next(reader, None) # skip header row

    for row in reader:
        x.append(row[0]) # key
        y.append(float(row[1])) # totalTime


# Generate graph
plt.bar(x, y, color = 'tab:blue', width = 0.72)
plt.xlabel('Input')
plt.ylabel('Total time (s)')
plt.title('Results')
plt.show()
