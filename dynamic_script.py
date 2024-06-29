import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read the CSV file into a DataFrame
df = pd.read_csv('output.csv')

# Get the correlation matrix of the DataFrame
corr_matrix = df.corr()

# Find the columns with the highest correlation
corr_matrix['Loyalty Reward Points'].sort_values(ascending=False)

# Plot the correlation matrix as a heatmap
plt.figure(figsize=(10,10))
sns.heatmap(corr_matrix, xticklabels=corr_matrix.columns, yticklabels=corr_matrix.columns,
annot=True, cmap='RdYlGn')
plt.title('Correlation Matrix of the DataFrame')
plt.savefig('static/graph.png')