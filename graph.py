import matplotlib.pyplot as plt

import os
import csv
import glob
from typing import List

from utils import print_wm1_intro

if __name__ == "__main__":
    print_wm1_intro()
    print("-> You are about to view a graph of the data from a session file.\n")

    csvFiles: List[str] = [file for file in glob.glob("data/*.csv")]
    """
    A list of files that are in the data directory and end in .csv. Each file in the list is in the format 'data/filename.csv'.
    """

    # Sort by file modification time, latest to earliest.
    csvFiles.sort(key=lambda file: os.path.getmtime(file), reverse=True)
    # Remove 'data/' prefix in each filename
    csvFiles = [os.path.basename(file) for file in csvFiles]

    HORIZONTAL_LINE = '-' * 40

    print('Data files:')
    print(HORIZONTAL_LINE)
    for filename in csvFiles:
        print(filename)
    print(HORIZONTAL_LINE)

    file = input("Enter the filename you want to analyze (you can copy and paste terminal text): ").strip()
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