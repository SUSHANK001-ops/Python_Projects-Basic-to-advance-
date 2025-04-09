# To do list (console base)
import os
Task = []
Task_End = True
print("""
      1.Add new task
      2.View Task
      3.Delete Task
      4:save in a file
      5.Exit
      """)


while Task_End:
    try:
        TasK_select = int(input("Enter an number to select Task:"))
        if TasK_select in [1,2,3,4,5]:
            pass
        else:
            print("Invalid option, please type 1, 2, 3, 4 or 5")
            continue
    except ValueError:
        print(f"This is not an valid number")   
        continue
    if TasK_select == 1:
        Add_Task = input("Enter your new Task:")
        Task.append(Add_Task)
    elif TasK_select == 2:
        for i in range(0,len(Task)):
            print(f"{i+1}:{Task[i]}")
    elif TasK_select ==3:
        try:
            b = int(input("Enter the task number to delete: "))
            if 1 <= b <= len(Task):
                Delete_Task = Task.pop(b-1)
                print(f"Deleted task: {Delete_Task}")
            else:
                print("Invalid task number")
        except (ValueError, IndexError):
            print("Please enter a valid task number")      
    elif TasK_select==4:
        file_path = r"D:\newpython\Save.txt"
        if os.path.exists(file_path):
            with open(file_path, "a") as file:
                for i in range(0,len(Task)):
                    file.write(f"{i+1}:{Task[i]}\n")
        else:
            with open(file_path, "w") as file:
                 for i in range(0,len(Task)):
                    file.write(f"{i+1}:{Task[i]}\n")
    elif TasK_select == 5:
        Task_End = False