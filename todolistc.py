import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

tasks = []

def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Message box is empty')
    else:
        tasks.append(task_string)
        the_cursor.execute('INSERT INTO tasks VALUES(?)', (task_string,))
        task_listbox.insert('end', task_string)
        task_field.delete(0, 'end')

def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            the_cursor.execute('DELETE FROM tasks WHERE title=?', (the_value,))
            task_listbox.delete('active')
    except tk.TclError:
        messagebox.showinfo('Error', 'No message selected. Cannot delete.')

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete all', 'Are you sure?')
    if message_box:
        task_listbox.delete(0, 'end')
        the_cursor.execute('DELETE FROM tasks')

def close():
    print(tasks)
    guiWindow.destroy()

def retrieve_database():
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])
        task_listbox.insert('end', row[0])

if __name__ == "__main__":
    guiWindow = tk.Tk()
    guiWindow.title("TO-DO LIST FOR DAILY ROUTINE")
    guiWindow.geometry("500x500+750+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#dffad7")

    the_connection = sql.connect('listOftasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks(title TEXT)')

    header_frame = tk.Frame(guiWindow, bg="#dffad7")
    functions_frame = tk.Frame(guiWindow, bg="#dffad7")
    listbox_frame = tk.Frame(guiWindow, bg="#dffad7")
    header_frame.pack(fill="both")
    functions_frame.pack(side="left", expand="true", fill="both")
    listbox_frame.pack(side="right", expand="true", fill="both")

    header_label = ttk.Label(
        header_frame,
        text="TO-DO-LIST",
        font=("Helvetica", "30"),
        background="#dafbd7",
        foreground="#000000"
    )
    header_label.pack(padx=20, pady=20)

    task_label = ttk.Label(
        functions_frame,
        text="Enter the task:",
        foreground="#dafbd7",
        background="#000000"
    )
    task_label.place(x=40, y=40)

    task_field = ttk.Entry(
        functions_frame,
        font=("Consolas", "12"),
        width=20,
        background="#822aa5",
        foreground="#a52aa5"
    )
    task_field.place(x=30, y=30)

    add_button = ttk.Button(
        functions_frame,
        text="Add task",
        width=26,
        command=add_task
    )
    del_button = ttk.Button(
        functions_frame,
        text="Delete task",
        width=26,
        command=delete_task
    )
    del_all_button = ttk.Button(
        functions_frame,
        text="Delete all tasks",
        width=26,
        command=delete_all_tasks
    )
    exit_button = ttk.Button(
        functions_frame,
        text="EXIT",
        width=26,
        command=close
    )

    add_button.place(x=30, y=70)
    del_button.place(x=30, y=110)
    del_all_button.place(x=30, y=150)
    exit_button.place(x=30, y=190)

    task_listbox = tk.Listbox(
        listbox_frame,
        width=28,
        height=14,
        selectmode="SINGLE",
        background="#FFFFFF",
        foreground="#000000",
        selectbackground="#59179c",
        selectforeground="#FFFFFF"
    )
    task_listbox.place(x=15, y=30)

    retrieve_database()

    guiWindow.mainloop()

    the_connection.commit()
    the_cursor.close()
