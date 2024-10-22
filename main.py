import tkinter as tk
from tkinter import ttk, messagebox
import csv
import re
import logging
import datetime

logging.basicConfig(filename="app_errors.log", level=logging.ERROR)

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

date = datetime.datetime.now()

# Function to handle saving the data to a CSV file
def save_data():
    date
    client_nameFirst = entry_nameFirst.get()
    client_nameLast = entry_nameLast.get()
    client_nameDog = entry_nameDog.get()
    client_email = entry_email.get()
    client_phone = entry_phone.get()
    selected_service = service_var.get()
    selected_goals = [goal for goal, var in goal_vars[selected_service].items() if var.get()]
    customGoals = entry_custom_goals.get()

    if not client_nameFirst or not client_nameLast:
        messagebox.showerror("Error", "Please fill out all client information fields.")
        return
    
    if not client_nameDog:
        messagebox.showerror("Error", "Please fill out all client information fields.")
        return
    
    if not client_email or not is_valid_email(client_email):
        messagebox.showerror("Error", "Please fill out all client information fields.")
        return
    
    if not client_phone:
        messagebox.showerror("Error", "Please fill out all client information fields.")
        return

    if not selected_goals:
        messagebox.showerror("Error", "Please select at least one training goal.")
        return
    

    # Save to CSV
    with open('dog_training_clients.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date,client_nameFirst, client_nameLast, client_nameDog, client_email, client_phone, selected_service, ', '.join(selected_goals), customGoals])

    messagebox.showinfo("Success", "Client information saved successfully!")
    # Clear the inputs after saving
    entry_nameFirst.delete(0, tk.END)
    entry_nameLast.delete(0, tk.END)
    entry_nameDog.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    for goal in goal_vars[selected_service].values():
        goal.set(False)
    entry_custom_goals.delete(0, tk.END)

# Function to update the available training goals based on the selected service
def update_goals(*args):
    selected_service = service_var.get()

    # Clear previous checkboxes
    for widget in goal_frame.winfo_children():
        widget.destroy()

    # Display new checkboxes for selected service
    goals = list(goal_vars[selected_service].keys())
    num_goals = len(goals)

    # Calculate mid-point for splitting into two rows
    mid_point = num_goals // 2 + num_goals % 2  # Ensures odd goals go to the first row

    for index, (goal, var) in enumerate(goal_vars[selected_service].items()):
        row = index // 2  # Two checkboxes per row
        column = index % 2  # Alternating columns
        tk.Checkbutton(goal_frame, text=goal, variable=var).grid(row=row, column=column, sticky='w')

    # Optionally, you may want to expand the goal_frame to fill available space
    goal_frame.update_idletasks()  # Update the frame to calculate its size
    goal_frame.config(height=row + 1)  # Set the height to accommodate two rows
    
def search_client():
    client_name = entry_search_name.get().strip().lower()
    
    if not client_name:
        messagebox.showerror("Error", "Please enter a client name.")
        return

    try:
        with open('dog_training_clients.csv', mode='r') as file:
            reader = csv.reader(file)
            found_clients = []
            
            for row in reader:
                full_name = f"{row[2].lower()} {row[3].lower()}"  # Combine first and last names
                if client_name in full_name:
                    found_clients.append(row)

        if found_clients:
            result_text.delete(1.0, tk.END)  # Clear previous results
            for client in found_clients:
                result_text.insert(tk.END, f"Date: {client[0]}\nUnique Id: {client[1]}\nClient: {client[2]} {client[3]}\nDog: {client[4]}\nEmail: {client[5]}\nPhone: {client[6]}\nService: {client[7]}\nGoals: {client[8]}\nCustom Goals: {client[9]}\n\n")
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "No matching client found.")

    except FileNotFoundError:
        messagebox.showerror("Error", "The CSV file was not found.")

def main():
    try:
        global entry_nameFirst, entry_nameLast, entry_nameDog, entry_email, entry_phone, goal_frame, goal_vars, service_var, entry_search_name, result_text, entry_custom_goals      

        # Tkinter setup
        root = tk.Tk()
        root.title("Dog Training Services")

        notebook = ttk.Notebook(root)
        addClientFrame = ttk.Frame(root)
        addSearchFrame = ttk.Frame(root)

        #Adding tabs to notebook
        notebook.add(addClientFrame, text="Add Client")
        notebook.add(addSearchFrame, text="Search Client")

        notebook.pack(expand=True, fill="both")

        # Define available services and their corresponding training goals
        services = {
            "Puppy Preschool": ["Potty Training", "Crate Training", "Nipping", "Barking", "Pawing", "Nudging", "Socialization","Sit", "Stay", "Down", "Come","Place"],
            "Basic Obedience": ["Potty Training", "Crate Training","Sit", "Stay", "Down", "Come", "Loose Leash Walking", "Place","Nipping", "Barking", "Pawing", "Nudging", "Socialization"],
            "Advanced Obedience": ["Potty Training", "Crate Training","Sit", "Stay", "Down", "Come", "Loose Leash Walking", "Place","Nipping", "Barking", "Pawing", "Nudging", "Socialization"],
            "Behavior Modification": ["Desensitization", "Counter-Conditioning","Counter Surfing","Escape Artist","Trash Thief","Heel", "Impulse Control","Potty Training", "Crate Training","Sit", "Stay", "Down", "Come", "Loose Leash Walking", "Place","Nipping", "Barking", "Pawing", "Nudging", "Socialization"],
        }

        # Variables to hold the current selected service and goals
        service_var = tk.StringVar(value="Puppy Preschool")
        goal_vars = {service: {goal: tk.BooleanVar() for goal in goals} for service, goals in services.items()}

        # Client Information Section
        tk.Label(addClientFrame, text="Client First Name:").grid(row=0, column=0, padx=10, pady=5)
        entry_nameFirst = tk.Entry(addClientFrame)
        entry_nameFirst.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(addClientFrame, text="Client Last Name:").grid(row=1, column=0, padx=10, pady=5)
        entry_nameLast = tk.Entry(addClientFrame)
        entry_nameLast.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(addClientFrame, text="Dog's Name:").grid(row=2, column=0, padx=10, pady=5)
        entry_nameDog = tk.Entry(addClientFrame)
        entry_nameDog.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(addClientFrame, text="Client Email:").grid(row=3, column=0, padx=10, pady=5)
        entry_email = tk.Entry(addClientFrame)
        entry_email.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(addClientFrame, text="Client Phone:").grid(row=4, column=0, padx=10, pady=5)
        entry_phone = tk.Entry(addClientFrame)
        entry_phone.grid(row=4, column=1, padx=10, pady=5)

        # Service Selection Section
        tk.Label(addClientFrame, text="Select Service:").grid(row=5, column=0, padx=10, pady=5)
        service_menu = ttk.OptionMenu(addClientFrame, service_var, "Puppy Preschool", *services.keys(), command=update_goals)
        service_menu.grid(row=5, column=1, padx=10, pady=5, sticky="nsew")

        # Training Goals Section
        tk.Label(addClientFrame, text="Select Training Goals:").grid(row=6, column=0, padx=10, pady=5)
        goal_frame = tk.Frame(addClientFrame)
        goal_frame.grid(row=6, column=1, padx=10, pady=5, sticky='nsew')  # Allow goal_frame to expand
        addClientFrame.grid_rowconfigure(6, weight=1)  # Allow row 6 to expand
        addClientFrame.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand

        # Entry for Custom Goals
        tk.Label(addClientFrame, text="Custom Goals:").grid(row=7, column=0, padx=10, pady=5)
        entry_custom_goals = tk.Entry(addClientFrame, width=40)
        entry_custom_goals.grid(row=7, column=1, padx=10, pady=5)

        # Initialize with the default service's goals
        update_goals()

        # Save Button
        save_button = tk.Button(addClientFrame, text="Save Client Data", command=save_data)
        save_button.grid(row=8, column=0, columnspan=2, pady=10, sticky="nsew")

         # --- Search Client Tab ---
        # Search Label and Entry
        tk.Label(addSearchFrame, text="Enter Client Name (First or Last):").pack(pady=10)
        entry_search_name = tk.Entry(addSearchFrame, width=40)
        entry_search_name.pack(pady=5)

        # Search Button
        search_button = tk.Button(addSearchFrame, text="Search", command=search_client)
        search_button.pack(pady=10)

        # Create a frame to hold the text box and the scrollbars
        result_frame = tk.Frame(addSearchFrame)
        result_frame.pack(pady=10)

        # Text widget to display the results
        result_text = tk.Text(result_frame, height=15, width=70, wrap=tk.NONE)
        result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        scrollbar_y = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar
        scrollbar_x = tk.Scrollbar(result_frame, orient=tk.HORIZONTAL, command=result_text.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure the text widget to use the scrollbars
        result_text.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        
        # Start the Tkinter event loop
        root.mainloop()

    except Exception as e:
        logging.error(f"Error in main application: {str(e)}")

if __name__ == "__main__":
    main()