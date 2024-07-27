import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('output.csv')

# Calculate the total profit for each month
df['total_profit'] = df['facecream'] + df['facewash'] + df['toothpaste'] + df['bathingsoap'] + df['shampoo'] + df['moisturizer']

# Create a pie chart of the total profit for each month
plt.pie(df['total_profit'], labels=df['month_number'])
plt.title('Total Profit by Month')
plt.xlabel('Month')
plt.ylabel('Total Profit')

# Save the plot as a PNG file
plt.savefig('static/graph.png')