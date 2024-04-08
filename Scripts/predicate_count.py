import matplotlib.pyplot as plt

# Data
# categories = ['Health effect', 'Disposition', 'Role', 'Process', 'Exposure Route', 'Food']
categories = ['causes', 'biolocation is', 'has role of', 'involved in', 'exposed through', 'sourced through']

values = [997050, 905195, 857181, 9596452, 53843, 4410057]

# Define colors for each bar
colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightseagreen', 'plum']

# Create bar graph
plt.figure(figsize=(10, 6))
plt.bar(categories, values, color=colors)

# Add labels and title
plt.xlabel('Predicates')
plt.ylabel('Count')
plt.title('Total Number of Triplets for Each Predicate')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show plot
plt.tight_layout()
plt.show()
