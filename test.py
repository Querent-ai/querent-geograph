import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Load your CSV data
data = pd.read_csv('/home/nishantg/Downloads/neo4j_query_table_data_2024-2-26.csv')  # Update the path to your CSV file
min_val = data['ShaleCount'].min()
max_val = data['ShaleCount'].max()
data['NormalizedShaleCount'] = (data['ShaleCount'] - min_val) / (max_val - min_val)

# Map normalized values to the 1cm to 5cm range for the radius
# 1cm = 28.35 points (in matplotlib, 1 inch = 72 points, and 1 inch ≈ 2.54 cm)
min_radius, max_radius = 28.35, 28.35 * 5
data['Radius'] = data['NormalizedShaleCount'].apply(lambda x: x * (max_radius - min_radius) + min_radius)

# Create a directory for the circle images
dir_name = '/home/nishantg/querent-main/geo/geo-timescale/images/circles'  # Update this to your desired path
os.makedirs(dir_name, exist_ok=True)

# Generate and save separate images for each circle
for index, row in data.iterrows():
    fig, ax = plt.subplots(figsize=(6, 6))  # Slightly larger figure to accommodate up to 5cm circles
    
    # Draw the circle with the calculated radius
    circle = plt.Circle((row['Radius'], row['Radius']), row['Radius'], color='blue', alpha=0.5)
    
    ax.add_patch(circle)
    # Adjust plot limits to ensure the full circle is visible
    ax.set_xlim(0, 2 * max_radius)
    ax.set_ylim(0, 2 * max_radius)
    ax.set_aspect('equal')
    ax.axis('off')
    # plt.title(row['GeologicalTime'])
    
    # Save the plot as an image file
    file_path = f"{dir_name}/{row['GeologicalTime'].replace('/', '_')}.png"
    plt.savefig(file_path, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()

# Output the directory path
print(dir_name)