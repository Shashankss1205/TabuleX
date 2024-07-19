import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('output.csv')

# Define the data types for each column
df['Customer ID'] = df['Customer ID'].astype(str)
df['Customer Name'] = df['Customer Name'].astype(str)
df['Loyalty Reward Points'] = df['Loyalty Reward Points'].astype(int)
df['Segment'] = df['Segment'].astype(str)
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')  # Converting Date to datetime
df['Fraction'] = df['Fraction'].astype(float)

# Create a scatter plot of 'Loyalty Reward Points' vs 'Fraction'
plt.scatter(df['Loyalty Reward Points'], df['Fraction'])

# Add a label to the x-axis
plt.xlabel('Loyalty Reward Points')

# Add a label to the y-axis
plt.ylabel('Fraction')

# Add a title to the plot
plt.title('Correlation between Loyalty Reward Points and Fraction')

# Save the plot as a PNG file
plt.savefig('static/graph.png')