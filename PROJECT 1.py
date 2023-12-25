import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json

TODO_FILE = "todo.json"

def load_todo():
    if not tk.messagebox.askyesno("Load To-Do List", "Load existing To-Do List?"):
        return {"tasks": []}

    if not tk.messagebox.askyesno("Load To-Do List", "Would you like to load from a file?"):
        return {"tasks": []}

    try:
        with open(TODO_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"tasks": []}

def save_todo(todo):
    with open(TODO_FILE, "w") as file:
        json.dump(todo, file, indent=2)

def show_todo():
    todo = load_todo()
    tasks = todo["tasks"]

    if not tasks:
        tk.messagebox.showinfo("To-Do List", "No tasks in the To-Do list.")
    else:
        task_list = "\n".join([f"{index + 1}. {task['title']} - {task['date']}" for index, task in enumerate(tasks)])
        tk.messagebox.showinfo("To-Do List", f"To-Do List:\n{task_list}")

def add_task():
    title = entry_title.get()
    date_str = entry_date.get()

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        tk.messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
        return

    todo = load_todo()
    tasks = todo["tasks"]

    tasks.append({"title": title, "date": date_str})
    save_todo(todo)
    tk.messagebox.showinfo("To-Do List", "Task added successfully!")
    entry_title.delete(0, tk.END)
    entry_date.delete(0, tk.END)

def remove_task():
    todo = load_todo()
    tasks = todo["tasks"]

    if not tasks:
        tk.messagebox.showinfo("To-Do List", "No tasks in the To-Do list.")
        return

    task_list = "\n".join([f"{index + 1}. {task['title']} - {task['date']}" for index, task in enumerate(tasks)])
    selected_index = tk.simpledialog.askinteger("Remove Task", f"Select the task to remove:\n{task_list}")

    if selected_index is None:
        return

    try:
        selected_index -= 1
        removed_task = tasks.pop(selected_index)
        save_todo(todo)
        tk.messagebox.showinfo("To-Do List", f"Task '{removed_task['title']}' removed successfully!")
    except (IndexError, ValueError):
        tk.messagebox.showerror("Error", "Invalid task index.")

# Main GUI window
root = tk.Tk()
root.title("To-Do List")

# Create and place widgets
label_title = tk.Label(root, text="Task Title:")
label_title.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

entry_title = tk.Entry(root, width=30)
entry_title.grid(row=0, column=1, padx=10, pady=10)

label_date = tk.Label(root, text="Due Date (YYYY-MM-DD):")
label_date.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

entry_date = tk.Entry(root, width=15)
entry_date.grid(row=1, column=1, padx=10, pady=10)

button_add = tk.Button(root, text="Add Task", command=add_task)
button_add.grid(row=2, column=0, columnspan=2, pady=10)

button_show = tk.Button(root, text="Show To-Do List", command=show_todo)
button_show.grid(row=3, column=0, columnspan=2, pady=10)

button_remove = tk.Button(root, text="Remove Task", command=remove_task)
button_remove.grid(row=4, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
