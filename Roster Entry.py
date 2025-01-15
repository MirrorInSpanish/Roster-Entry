import tkinter as tk
from tkinter import messagebox
import psycopg2

# Function to check non-letter characters
def check_non_letter(name):
    return not name.isalpha()

# Function to handle form submission
def submit_form():
    first_name = entry_firstname.get()
    last_name = entry_lastname.get()
    age = entry_age.get()
    height = entry_height.get()

    # Validation for name
    if not first_name or check_non_letter(first_name):
        messagebox.showerror("Input Error", "Only letters are allowed for the first name.")
        return
    
    # Validation for last name
    if not last_name or check_non_letter(last_name):
        messagebox.showerror("Input Error", "Only letters are allowed for the last name.")
        return
    
    # Validation for age
    try:
        age = float(age)
        if age <= 0 or age >= 100:
            messagebox.showerror("Input Error", "Age must be between 1 and 99.")
            return
        age = int(age)  # Remove decimal
    except ValueError:
        messagebox.showerror("Input Error", "Only numbers are allowed for age.")
        return

    # Validation for height
    try:
        height = float(height)
        if height <= 0 or height >= 8:
            messagebox.showerror("Input Error", "Height must be between 0 and 8 feet.")
            return
    except ValueError:
        messagebox.showerror("Input Error", "Only numbers are allowed for height.")
        return

    # Connect to Neon PostgreSQL and save data
    try:
        conn = psycopg2.connect(
            "postgresql://Roster_owner:8qTRoUFH5hxD@ep-lingering-truth-a5c1ym6f.us-east-2.aws.neon.tech/Roster?sslmode=require"
        )
        cursor = conn.cursor()

        # Insert the data into the database
        cursor.execute(
            "INSERT INTO users (first_name, last_name, age, height) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, age, height)
        )
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "User information saved to the Neon database!")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    # Clear input fields after submission
    entry_firstname.delete(0, tk.END)
    entry_lastname.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_height.delete(0, tk.END)
    
    # Display user info
    display_user_info()

# Function to display user information
def display_user_info():
    result_text.delete('1.0', tk.END)
    for i, user in enumerate(user_info, start=1):
        result_text.insert(tk.END, f"\nUser {i}:\n")
        result_text.insert(tk.END, f"Your first name is {user['first_name']}\n")
        result_text.insert(tk.END, f"Your last name is {user['last_name']}\n")
        result_text.insert(tk.END, f"You are {user['age']} years old.\n")
        result_text.insert(tk.END, f"Your height is {user['height']} feet.\n")

# Main application window
root = tk.Tk()
root.title("User Information Form")

# Input fields
tk.Label(root, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
entry_firstname = tk.Entry(root)
entry_firstname.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
entry_lastname = tk.Entry(root)
entry_lastname.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Age (1-99):").grid(row=2, column=0, padx=5, pady=5)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Height (0-8 feet):").grid(row=3, column=0, padx=5, pady=5)
entry_height = tk.Entry(root)
entry_height.grid(row=3, column=1, padx=5, pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=4, columnspan=2, pady=10)

# Result display
result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

user_info = []

# Run the Tkinter event loop
root.mainloop()
