import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

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

def on_calculate():
    try:
        A = int(A_entry.get())
        T = float(T_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid values for A and T.")
        return
    
    z_matrix = read_csv_and_extract_z(file_path)
    row_diff_matrix, col_diff_matrix = calculate_height_differences(z_matrix, A)
    
    visualize_matrix(row_diff_matrix, T, "Row-wise Height Difference Matrix")
    visualize_matrix(col_diff_matrix, T, "Column-wise Height Difference Matrix")

def visualize_matrix(matrix, threshold, title):
    rows, cols = matrix.shape
    
    matrix_window = tk.Toplevel(root)
    matrix_window.title(title)
    
    canvas = tk.Canvas(matrix_window, width=cols*30, height=rows*30)
    canvas.pack()
    
    for i in range(rows):
        for j in range(cols):
            value = matrix[i, j]
            color = 'red' if abs(value) > threshold else 'black'
            canvas.create_text(j * 30 + 15, i * 30 + 15, text=f"{value:.2f}", fill=color)

root = tk.Tk()
root.title("Height Difference Calculator")

file_path = 'D:/1-ZEUGS-/PunkteAuslesen/Boden_50cm_Punkte.txt'  # Replace with the path to your file

# Input fields for A and T
ttk.Label(root, text="Step Distance A:").grid(row=0, column=0, padx=5, pady=5)
A_entry = ttk.Entry(root)
A_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Threshold T:").grid(row=1, column=0, padx=5, pady=5)
T_entry = ttk.Entry(root)
T_entry.grid(row=1, column=1, padx=5, pady=5)

# Calculate button
calculate_button = ttk.Button(root, text="Calculate", command=on_calculate)
calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
