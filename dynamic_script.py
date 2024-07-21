import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read the data from the CSV file
data = pd.read_csv('output.csv')

# Get the total profit column
total_profit = data['total_profit']

# Draw the histogram
plt.hist(total_profit, bins=20)
plt.xlabel('Total Profit')
plt.ylabel('Frequency')
plt.title('Histogram of Total Profit')

# Save the plot as a PNG file
plt.savefig('static/graph.png')