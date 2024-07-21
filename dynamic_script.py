import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the CSV file
df = pd.read_csv('output.csv')

# Get the total profit for each month
total_profit = df['total_profit'].values

# Create a pie chart
plt.pie(total_profit, labels=df['month_number'].values, autopct='%1.1f%%')
plt.title('Total Profit by Month')
plt.savefig('static/graph.png')
plt.show()