import matplotlib.pyplot as plt
import pandas as pd

# Read the sales data
sales = pd.read_csv('output.csv')

# Create a scatter plot of sales over time
plt.scatter(sales['date_of_purchase'], sales['purchase_number'])

# Label the axes
plt.xlabel('Date of Purchase')
plt.ylabel('Purchase Number')

# Set a title for the plot
plt.title('Sales Over Time')

# Save the plot as a PNG image
plt.savefig('static/graph.png')