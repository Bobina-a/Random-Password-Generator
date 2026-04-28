import random
import string
import json
import os
from tkinter import *
from tkinter import ttk, messagebox

HISTORY_FILE = "password_history.json"

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Переменные
        self.length = IntVar(value=12)
        self.use_digits = BooleanVar(value=True)
        self.use_letters = BooleanVar(value=True)
        self.use_symbols = BooleanVar(value=True)
        self.history = self.load_history()

        # Интерфейс
        self.create_widgets()
        self.update_history_table()

    def create_widgets(self):
        # Рамка настроек
        settings_frame = LabelFrame(self.root, text="Настройки пароля", padx=10, pady=10)
        settings_frame.pack(fill="x", padx=10, pady=5)

        # Длина пароля
        Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky="w")
        Scale(settings_frame, from_=4, to=32, orient=HORIZONTAL, variable=self.length, length=300).grid(row=0, column=1, padx=10)
        Label(settings_frame, textvariable=self.length).grid(row=0, column=2)

        # Чекбоксы
        Checkbutton(settings_frame, text="Буквы (A-Z, a-z)", variable=self.use_letters).grid(row=1, column=0, columnspan=2, sticky="w")
        Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=2, column=0, columnspan=2, sticky="w")
        Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&* etc.)", variable=self.use_symbols).grid(row=3, column=0, columnspan=2, sticky="w")

        # Кнопка генерации
        Button(self.root, text="Сгенерировать пароль", command=self.generate, bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

        # Поле для отображения пароля
        self.password_var = StringVar()
        entry_frame = Frame(self.root)
        entry_frame.pack(fill="x", padx=10, pady=5)
        Entry(entry_frame, textvariable=self.password_var, font=("Courier", 14), state="readonly", readonlybackground="white").pack(side="left", fill="x", expand=True)
        Button(entry_frame, text="Копировать", command=self.copy_to_clipboard).pack(side="right", padx=5)

        # Таблица истории
        Label(self.root, text="История паролей:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        self.tree = ttk.Treeview(self.root, columns=("password", "length", "charset"), show="headings", height=10)
        self.tree.heading("password", text="Пароль")
        self.tree.heading("length", text="Длина")
        self.tree.heading("charset", text="Тип символов")
        self.tree.column("password", width=300)
        self.tree.column("length", width=80)
        self.tree.column("charset", width=200)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Кнопки управления историей
        btn_frame = Frame(self.root)
        btn_frame.pack(pady=5)
        Button(btn_frame, text="Очистить историю", command=self.clear_history, bg="red", fg="white").pack(side="left", padx=5)
        Button(btn_frame, text="Сохранить в JSON", command=self.save_history_to_file).pack(side="left", padx=5)

    def get_char_pool(self):
        pool = ""
        if self.use_letters.get():
            pool += string.ascii_letters
        if self.use_digits.get():
            pool += string.digits
        if self.use_symbols.get():
            pool += string.punctuation
        return pool

    def generate(self):
        pool = self.get_char_pool()
        if not pool:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        length = self.length.get()
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа")
            return
        if length > 32:
            messagebox.showerror("Ошибка", "Максимальная длина пароля — 32 символа")
            return
        password = ''.join(random.choice(pool) for _ in range(length))
        self.password_var.set(password)

        # Сохраняем в историю
        charset = ""
        if self.use_letters.get(): charset += "буквы "
        if self.use_digits.get(): charset += "цифры "
        if self.use_symbols.get(): charset += "символы"
        self.history.insert(0, {"password": password, "length": length, "charset": charset.strip()})
        if len(self.history) > 50:
            self.history = self.history[:50]
        self.save_history_to_file()
        self.update_history_table()

    def update_history_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.history[:20]:
            self.tree.insert("", "end", values=(item["password"], item["length"], item["charset"]))

    def copy_to_clipboard(self):
        pwd = self.password_var.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history_to_file(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def clear_history(self):
        self.history = []
        self.save_history_to_file()
        self.update_history_table()
        messagebox.showinfo("Очищено", "История удалена")

if __name__ == "__main__":
    root = Tk()
    app = PasswordGenerator(root)
    root.mainloop()