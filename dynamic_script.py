import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the csv file into a dataframe
df = pd.read_csv('output.csv')

# Create a graph of the employee data
sns.barplot(data=df, x='name', y='age')

# Save the plot as a png file
plt.savefig('static/graph.png')