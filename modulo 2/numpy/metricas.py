import numpy as np
import matplotlib.pyplot as plt
import glob

# Define the path pattern for the .dat files
file_pattern = '*.dat'

# Get a list of file paths matching the pattern
file_paths = glob.glob(file_pattern)

# Initialize an empty list to store the data arrays
data_arrays = []

# Load data from each file into separate arrays
for file_path in file_paths:
    data = np.loadtxt(file_path)
    data_arrays.append(data)

# Combine the arrays into a single 2D array
combined_data = np.vstack(data_arrays)

# Calculate the correlation matrix
correlation_matrix = np.corrcoef(combined_data, rowvar=False)

# Flatten the correlation matrix and sort the values in descending order
sorted_correlation = np.sort(correlation_matrix.flatten())[::-1]

# Number of highest correlations to display
n = 5

# Select the top n highest correlations
top_n_correlation = sorted_correlation[:n]

# Get the indices of the top n correlations in the flattened matrix
row_indices, col_indices = np.unravel_index(np.argsort(correlation_matrix, axis=None)[::-1], correlation_matrix.shape)

# Print the top n highest correlations and the corresponding file names
print(f"Top {n} highest correlations:")
for i in range(n):
    row_index = row_indices[i]
    col_index = col_indices[i]
    correlation_value = correlation_matrix[row_index, col_index]
    file1 = file_paths[row_index]
    file2 = file_paths[col_index]
    print(f"{file1} - {file2}: {correlation_value:.4f}")

# Create a figure and axes
fig, ax = plt.subplots()

# Create a heatmap
heatmap = ax.imshow(correlation_matrix, cmap='coolwarm')

# Set the tick labels and show them on all axes
ax.set_xticks(np.arange(len(file_paths)))
ax.set_yticks(np.arange(len(file_paths)))
ax.set_xticklabels(file_paths, rotation=45, ha='right')
ax.set_yticklabels(file_paths)

# Add colorbar
cbar = plt.colorbar(heatmap)

# Set the title
ax.set_title('Correlation Matrix')

# Show the plot
plt.show()
