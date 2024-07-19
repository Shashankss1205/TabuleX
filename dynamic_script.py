import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the CSV file
df = pd.read_csv('output.csv')

# Extract the data for the bar chart
total_profit = df['total_profit']
month_number = df['month_number']

# Create the bar chart
plt.bar(month_number, total_profit, color=['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'black'])

# Set the title and labels for the chart
plt.title('Total Profit by Month')
plt.xlabel('Month Number')
plt.ylabel('Total Profit')

# Save the plot as a PNG file
plt.savefig('static/graph.png')