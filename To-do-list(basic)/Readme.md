# 📝 Console-Based To-Do List

A basic Python program that allows users to manage a to-do list via the command line. Users can add, view, delete, and save tasks to a file.

## 📌 Features

- ✅ Add new tasks  
- 📋 View current tasks  
- ❌ Delete tasks by number  
- 💾 Save tasks to a text file  
- 🚪 Exit the program  

## 🚀 How to Run

1. Make sure you have **Python 3** installed.
2. Copy the script to a `.py` file (e.g., `todo.py`).
3. Open your terminal or command prompt.
4. Run the script using:
   ```bash
   python todo.py
   ```

## 📂 File Save Location

Saved tasks are written to:

```
D:\newpython\Save.txt
```

Make sure this directory exists or update the path in the code to match your own system.

## 🧠 Sample Menu

```
      1. Add new task
      2. View Task
      3. Delete Task
      4. Save in a file
      5. Exit
```

## ✅ Example Usage

1. **Add a Task**  
   Input: `1`  
   Prompt: `Enter your new Task:`  
   Result: Adds task to your list

2. **View Tasks**  
   Input: `2`  
   Output: Displays all tasks with numbers

3. **Delete a Task**  
   Input: `3`  
   Prompt: `Enter the task number to delete:`  
   Result: Deletes the task if the number is valid

4. **Save Tasks**  
   Input: `4`  
   Result: Appends or writes the task list to a file

5. **Exit**  
   Input: `5`  
   Result: Exits the application

## 🛠 Requirements

- Python 3.x
- No external libraries needed

## 🧹 Future Improvements
- A GUI base interface
- Prevent duplicate entries
- Add a confirmation before exiting
- Load saved tasks on startup
- Timestamp for tasks
- Mark tasks as completed
