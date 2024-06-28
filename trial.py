s= '''
```python
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('output.csv')

# Create a bar chart of the customers and their fractions
df.plot.bar(x='Customer Name', y='Fraction')

# Set the title of the chart
plt.title('Customer Fractions')

# Show the chart
plt.show()
'''
print(s.find('```python'))