import matplotlib.pyplot as plt

import os
import csv
from glob import glob


csvFiles = [os.path.basename(file) for file in glob("data/*.csv")]
"""
A list of filenames of files that are in the data directory and end in .csv.
"""

horizontalLine = '-' * 40

print('Data files:')
print(horizontalLine)
for filename in csvFiles:
    print(filename)
print(horizontalLine)

file = input("Enter the filename you want to analyze: ").strip()
if file not in csvFiles:
    raise FileNotFoundError(f"{file}")


x = []
y = []

with open(os.path.join('data', file), 'r') as csvFile:
    reader = csv.reader(csvFile)
    next(reader, None) # skip header row

    for row in reader:
        x.append(row[0]) # key
        y.append(float(row[1])) # totalTime

plt.bar(x, y, color = 'g', width = 0.72, label = "Keys")
plt.xlabel('Key')
plt.ylabel('Total Time')
plt.title('Results')
plt.legend()
plt.show()