import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the data from the CSV file
df = pd.read_csv('output.csv')

# Create a donut chart of the data
plt.pie(df['Fraction'], labels=df['Segment'], autopct='%1.1f%%')
plt.title('Donut Chart of Customer Segments')

# Save the plot as a PNG file
plt.savefig('static/graph.png')