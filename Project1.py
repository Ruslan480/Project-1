import tkinter as tk
import sqlite3

# Создание и подключение к базе данных
conn = sqlite3.connect('employees.db')
cur = conn.cursor()

# Создание таблицы сотрудников, если она не существует
cur.execute('''CREATE TABLE IF NOT EXISTS employees
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                salary REAL)''')
conn.commit()

# Инициализация списка сотрудников
root = tk.Tk()
employee_listbox = tk.Listbox(root)


def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    # Вставка нового сотрудника в базу данных
    cur.execute('''INSERT INTO employees (name, phone, email, salary)
                   VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
    conn.commit()

    # Очистка полей ввода
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)

    # Добавление нового сотрудника в список
    employee_listbox.insert(tk.END, name)


def update_employee():
    selected_employee = employee_listbox.get(tk.ACTIVE)
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    # Обновление информации о выбранном сотруднике в базе данных
    cur.execute('''UPDATE employees
                   SET name=?, phone=?, email=?, salary=?
                   WHERE name=?''', (name, phone, email, salary, selected_employee))
    conn.commit()

    # Обновление информации о выбранном сотруднике в списке
    employee_listbox.delete(tk.ACTIVE)
    employee_listbox.insert(tk.ACTIVE, name)


def delete_employee():
    selected_employee = employee_listbox.get(tk.ACTIVE)

    # Удаление выбранного сотрудника из базы данных
    cur.execute('DELETE FROM employees WHERE name=?', (selected_employee,))
    conn.commit()

    # Удаление выбранного сотрудника из списка
    employee_listbox.delete(tk.ACTIVE)


def search_employee():
    search_name = search_entry.get()

    # Поиск сотрудников по ФИО
    cur.execute("SELECT name, phone, email, salary FROM employees WHERE name LIKE ?", ('%' + search_name + '%',))
    employees = cur.fetchall()

    # Очистка текущего списка сотрудников
    employee_listbox.delete(0, tk.END)

    # Добавление найденных сотрудников в список
    for employee in employees:
        employee_listbox.insert(tk.END, employee[0])


def select_employee(event):
    selected_employee = employee_listbox.get(tk.ACTIVE)

    # Получение информации о выбранном сотруднике
    cur.execute("SELECT name, phone, email, salary FROM employees WHERE name=?", (selected_employee,))
    employee = cur.fetchone()  # Изменение в этой строке

    # Заполнение полей ввода информацией о выбранном сотруднике
    name_entry.delete(0, tk.END)
    name_entry.insert(tk.END, employee[0])

    phone_entry.delete(0, tk.END)
    phone_entry.insert(tk.END, employee[1])

    email_entry.delete(0, tk.END)
    email_entry.insert(tk.END, employee[2])

    salary_entry.delete(0, tk.END)
    salary_entry.insert(tk.END, employee[3])


root.title('Список сотрудников компании')

# Создание элементов интерфейса
tk.Label(root, text='ФИО:').grid(row=0, column=0)
tk.Label(root, text='Номер телефона:').grid(row=1, column=0)
tk.Label(root, text='Email:').grid(row=2, column=0)
tk.Label(root, text='Заработная плата:').grid(row=3, column=0)

name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

phone_entry = tk.Entry(root)
phone_entry.grid(row=1, column=1)

email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

salary_entry = tk.Entry(root)
salary_entry.grid(row=3, column=1)

add_button = tk.Button(root, text='Добавить', command=add_employee)
add_button.grid(row=4, column=0)

update_button = tk.Button(root, text='Изменить', command=update_employee)
update_button.grid(row=4, column=1)

delete_button = tk.Button(root, text='Удалить', command=delete_employee)
delete_button.grid(row=5, column=0)

search_entry = tk.Entry(root)
search_entry.grid(row=5, column=1)

root.mainloop()

conn.close()