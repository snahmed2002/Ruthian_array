import tkinter as tk
from tkinter import messagebox
import numpy as np

def build_routh_array(coefficients):
    n = len(coefficients)
    rows = (n + 1) // 2  # Number of rows in the Routh array
    routh_array = np.zeros((n, rows))

    # Fill the first two rows of the Routh array
    routh_array[0, :len(coefficients[::2])] = coefficients[::2]
    routh_array[1, :len(coefficients[1::2])] = coefficients[1::2]

    # Calculate the rest of the Routh array
    for i in range(2, n):
        for j in range(rows - 1):
            if routh_array[i - 1, 0] == 0:  # Handling zero in the first column
                routh_array[i - 1, 0] = 1e-12  # Substitute a small value (epsilon)
            
            routh_array[i, j] = (routh_array[i - 1, 0] * routh_array[i - 2, j + 1] -
                                 routh_array[i - 2, 0] * routh_array[i - 1, j + 1]) / routh_array[i - 1, 0]
        
        # Stop the loop if the entire row is zero (auxiliary polynomial case)
        if np.all(routh_array[i, :] == 0):
            break
    
    return routh_array

def check_stability(routh_array):
    first_column = routh_array[:, 0]
    
    # Check for any sign changes in the first column
    sign_changes = np.sum(np.sign(first_column[:-1]) != np.sign(first_column[1:]))
    
    if sign_changes == 0:
        return True, sign_changes  # Stable system
    else:
        return False, sign_changes  # Unstable system

def routh_hurwitz_stability(coefficients):
    try:
        # Convert input coefficients to list of floats
        coefficients = [float(i) for i in coefficients]
        
        # Build the Routh array
        routh_array = build_routh_array(coefficients)
        
        # Check system stability
        stable, sign_changes = check_stability(routh_array)
        
        # Display the Routh array and stability results in a new window
        result_window = tk.Toplevel()
        result_window.title("Routh Array and Stability Analysis")
        
        result_label = tk.Label(result_window, text="Routh Array:")
        result_label.pack(pady=10)
        
        # Display Routh array
        array_str = ""
        for row in routh_array:
            array_str += str(row) + "\n"
        array_text = tk.Text(result_window, height=10, width=50)
        array_text.pack(padx=10, pady=10)
        array_text.insert(tk.END, array_str)
        array_text.config(state=tk.DISABLED)  # Disable editing
        
        # Display stability result
        stability_label = tk.Label(result_window, text="")
        stability_label.pack(pady=10)
        
        if stable:
            stability_label.config(text="The system is stable.", fg="green")
        else:
            stability_label.config(text=f"The system is unstable. Number of right-half plane poles: {sign_changes}", fg="red")
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric coefficients.")

def submit_coefficients():
    # Get input coefficients from entry field and split them
    coeffs = entry.get().split()
    
    if coeffs:
        routh_hurwitz_stability(coeffs)
    else:
        messagebox.showerror("Input Error", "Please enter the coefficients.")

# Main GUI window setup
root = tk.Tk()
root.title("Routh-Hurwitz Stability Calculator")

# Instructions
instruction_label = tk.Label(root, text="Enter the coefficients of the characteristic equation:")
instruction_label.pack(pady=10)

# Entry box for coefficients
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_coefficients)
submit_button.pack(pady=10)

# Run the application
root.mainloop()
