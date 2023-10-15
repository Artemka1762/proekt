import sqlite3
import tkinter as tk
from tkinter import ttk

# Создаем базу данных SQLite для хранения сотрудников
conn = sqlite3.connect("employee_db.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    salary REAL)''')
conn.commit()

# Создаем графический интерфейс с использованием библиотеки tkinter
root = tk.Tk()
root.title("Список сотрудников компании")

# Функция для добавления нового сотрудника
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)",
                   (name, phone, email, salary))
    conn.commit()
    clear_entries()
    display_records()

# Функция для обновления информации о сотруднике
def update_employee():
    selected_item = tree.selection()
    if selected_item:
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = salary_entry.get()
        emp_id = tree.item(selected_item)["values"][0]

        cursor.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?",
                       (name, phone, email, salary, emp_id))
        conn.commit()
        clear_entries()
        display_records()

# Функция для удаления сотрудника
def delete_employee():
    selected_item = tree.selection()
    if selected_item:
        emp_id = tree.item(selected_item)["values"][0]
        cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        conn.commit()
        clear_entries()
        display_records()

# Функция для поиска сотрудника по ФИО
def search_employee():
    search_name = search_entry.get()
    cursor.execute("SELECT * FROM employees WHERE name=?", (search_name,))
    records = cursor.fetchall()
    display_records(records)

# Функция для очистки полей ввода
def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)

# Функция для отображения записей в виджете Treeview
def display_records(records=None):
    if not records:
        cursor.execute("SELECT * FROM employees")
        records = cursor.fetchall()

    tree.delete(*tree.get_children())
    for row in records:
        tree.insert("", "end", values=row)

# Создаем и настраиваем интерфейс
name_label = tk.Label(root, text="ФИО:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

phone_label = tk.Label(root, text="Телефон:")
phone_label.grid(row=1, column=0)
phone_entry = tk.Entry(root)
phone_entry.grid(row=1, column=1)

email_label = tk.Label(root, text="Email:")
email_label.grid(row=2, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

salary_label = tk.Label(root, text="Заработная плата:")
salary_label.grid(row=3, column=0)
salary_entry = tk.Entry(root)
salary_entry.grid(row=3, column=1)

add_button = tk.Button(root, text="Добавить", command=add_employee)
add_button.grid(row=4, column=0)

update_button = tk.Button(root, text="Обновить", command=update_employee)
update_button.grid(row=4, column=1)

delete_button = tk.Button(root, text="Удалить", command=delete_employee)
delete_button.grid(row=4, column=2)

search_label = tk.Label(root, text="Поиск по ФИО:")
search_label.grid(row=5, column=0)
search_entry = tk.Entry(root)
search_entry.grid(row=5, column=1)
search_button = tk.Button(root, text="Найти", command=search_employee)
search_button.grid(row=5, column=2)

tree = ttk.Treeview(root, columns=("ID", "ФИО", "Телефон", "Email", "Заработная плата"))
tree.heading("ID", text="ID")
tree.heading("ФИО", text="ФИО")
tree.heading("Телефон", text="Телефон")
tree.heading("Email", text="Email")
tree.heading("Заработная плата", text="Заработная плата")
tree.grid(row=6, column=0, columnspan=3)

display_records()

root.mainloop()
