import numpy as np

def read_csv_and_extract_z(file_path):
    z_matrix = []
    current_row = []
    last_x = None
    
    with open(file_path, 'r') as file:
        for line in file:
            row = line.strip().split(',')
            x = float(row[1])
            z = float(row[3])
            
            if last_x is None:
                last_x = x
            
            if x != last_x:
                z_matrix.append(current_row)
                current_row = []
                last_x = x
            
            current_row.append(z)
        
        if current_row:
            z_matrix.append(current_row)
    
    return np.array(z_matrix)

def calculate_height_differences(matrix, A):
    rows, cols = matrix.shape
    max_row_diff_matrix = np.zeros(matrix.shape)
    max_col_diff_matrix = np.zeros(matrix.shape)
    A = A - 1  # Adjust for 0-based indexing
    
    # Calculate row-wise height differences
    for i in range(rows):
        for j in range(cols - A):
            diff = matrix[i, j + A] - matrix[i, j]
            step = diff / A
            for k in range(1, A):
                deviation = matrix[i, j] + step * k - matrix[i, j + k]
                if abs(deviation) > abs(max_row_diff_matrix[i, j + k]):
                    max_row_diff_matrix[i, j + k] = deviation
    
    # Calculate column-wise height differences
    for j in range(cols):
        for i in range(rows - A):
            diff = matrix[i + A, j] - matrix[i, j]
            step = diff / A
            for k in range(1, A):
                deviation = matrix[i, j] + step * k - matrix[i + k, j]
                if abs(deviation) > abs(max_col_diff_matrix[i + k, j]):
                    max_col_diff_matrix[i + k, j] = deviation
    
    return max_row_diff_matrix, max_col_diff_matrix

file_path = 'D:/1-ZEUGS-/PunkteAuslesen/Boden_50cm_Punkte.txt'  # Replace with the path to your file
z_matrix = read_csv_and_extract_z(file_path)

A = 4  # Set the distance A
height_diff_matrices = calculate_height_differences(z_matrix, A)

# Debug

#print("Original Z Matrix:")
#print(z_matrix)

#for idx, mat in enumerate(height_diff_matrices):
#    print(f"Height Difference Matrix {idx + 1}:")
#    print(mat)