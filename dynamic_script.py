import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the data from the CSV file
df = pd.read_csv("output.csv")

# Create a bar chart of the fruits and their stock units
df['Fruit'].value_counts()[:10].plot(kind='bar')
plt.title("Top 10 Fruits by Stock Units")
plt.xlabel("Fruit")
plt.ylabel("Stock Units")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("static/graph.png")  # Save the plot as an image