import tkinter as tk
from tkinter import ttk, messagebox, END, HORIZONTAL
import random
import string
import json

HISTORY_FILE = "history.json"
password_history = []

# --- Работа с JSON ---
def load_history():
    global password_history
    try:
        with open(HISTORY_FILE, "r") as f:
            password_history = json.load(f)
    except FileNotFoundError:
        password_history = []
    update_history_table()

def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(password_history, f, indent=2)

# --- Логика генерации ---
def generate_password():
    length = scale_length.get()
    use_lower = var_lower.get()
    use_upper = var_upper.get()
    use_digits = var_digits.get()
    use_symbols = var_symbols.get()
    
    # Проверка: выбран хотя бы один тип символов
    if not (use_lower or use_upper or use_digits or use_symbols):
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
        return

    chars = ""
    if use_lower: chars += string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_symbols: chars += string.punctuation

    password = ''.join(random.choices(chars, k=length))
    entry_password.delete(0, END)
    entry_password.insert(0, password)
    
    # Добавление в историю (только если пароль не пустой)
    if password:
        password_history.append(password)
        save_history()
        update_history_table()

def clear_history():
    global password_history
    confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?")
    if confirm:
        password_history = []
        save_history()
        update_history_table()
        messagebox.showinfo("Успех", "История очищена!")

def update_history_table():
    for i in treeview_history.get_children():
        treeview_history.delete(i)
    for pwd in password_history:
        treeview_history.insert("", END, values=(pwd))


# --- GUI ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("700x500")
root.resizable(False, False)
root.configure(bg="#f5f5f5")


# --- Параметры ---
frame_params = tk.LabelFrame(root, text="Параметры пароля", bg="#f5f5f5", padx=10, pady=10)
frame_params.pack(pady=10, padx=15, fill=tk.X)

# Ползунок длины
tk.Label(frame_params, text="Длина:", bg="#f5f5f5").grid(row=0, column=0, sticky="e")
scale_length = tk.Scale(frame_params, from_=4, to=32, orient=HORIZONTAL, length=200)
scale_length.set(12)
scale_length.grid(row=0, column=1, columnspan=2, pady=5)


# Чекбоксы символов
var_lower = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(frame_params, text="a-z", variable=var_lower, bg="#f5f5f5").grid(row=1, column=0)
tk.Checkbutton(frame_params, text="A-Z", variable=var_upper, bg="#f5f5f5").grid(row=1, column=1)
tk.Checkbutton(frame_params, text="0-9", variable=var_digits, bg="#f5f5f5").grid(row=2, column=0)
tk.Checkbutton(frame_params, text="!@#$", variable=var_symbols, bg="#f5f5f5").grid(row=2, column=1)


# --- Кнопки и вывод ---
frame_buttons = tk.Frame(root, bg="#f5f5f5")
frame_buttons.pack(pady=10)

btn_generate = tk.Button(frame_buttons, text="Сгенерировать пароль", command=generate_password)
btn_generate.pack(side=tk.LEFT, padx=10)

btn_clear_hist = tk.Button(frame_buttons, text="Очистить историю", command=clear_history)
btn_clear_hist.pack(side=tk.RIGHT, padx=10)


# Поле вывода пароля
frame_output = tk.Frame(root)
frame_output.pack(pady=10)
tk.Label(frame_output, text="Ваш пароль:").pack(side=tk.LEFT)
entry_password = tk.Entry(frame_output, width=40, font=('Arial', 12))
entry_password.pack(side=tk.LEFT, padx=10)


# --- История ---
frame_history = tk.LabelFrame(root, text="История паролей", bg="#f5f5f5", padx=10, pady=10)
frame_history.pack(pady=10, padx=15, fill='both', expand=True)

columns = ("Пароль",)
treeview_history = ttk.Treeview(frame_history, columns=columns, show='headings')
treeview_history.heading("Пароль", text="Пароль")
treeview_history.column("Пароль", width=600)
treeview_history.pack(fill='both', expand=True)


# Запуск загрузки истории при старте приложения и запуск главного цикла
load_history()
root.mainloop()
