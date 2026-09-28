import customtkinter as ctk
import threading
from tkinter import filedialog
from sort import sort_my_files

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Настройка окна
app = ctk.CTk()
app.title("MySorter")
app.geometry("800x600")
app.resizable(width=False, height=False)
app.iconbitmap("icon.ico")

# Функция для кнопки старт
def start_sort():
    folder_from = folder_entry.get().strip()
    folder_to = output_folder_entry.get().strip()
    start_button.configure(state="disabled")
    progress.set(0)
    progress_label.configure(text="0%")
    threading.Thread(
        target=sort_my_files,
        args=(folder_from, folder_to, log_label, progress, progress_label),
        daemon=True,
        name="sorter"
    ).start()
    check_thread()

# Проверка что поток завершен
def check_thread():
    if any(t.name == "sorter" and t.is_alive() for t in threading.enumerate()):
        app.after(200, check_thread)
    else:
        start_button.configure(state="normal")
    
# Функция для выбора папки с обзором
def browse_from():
    path = filedialog.askdirectory()
    if path:
        folder_entry.delete(0, "end")
        folder_entry.insert(0, path)

# Функция для выбора папки вывода с обзором
def browse_to():
    path = filedialog.askdirectory()
    if path:
        output_folder_entry.delete(0, "end")
        output_folder_entry.insert(0, path)
        
# Заголовок
title_label = ctk.CTkLabel(
    master=app,
    text="MySorter - сортировщик папки",
    font=("Segoe UI", 24, "bold"),
    text_color="#f8b015",
    fg_color="#3f3f3f",
    corner_radius=8
)
title_label.place(x=200, y=20)

# Текст ввода
folder_label = ctk.CTkLabel(
    master=app,
    text='Укажите папку сортировки к примеру "C:\\sandbox\\"',
    font=("Arial", 14, "bold"),
    text_color="#f8b015"
)
folder_label.place(x=20, y=120)

# Текст вывода
output_folder_label = ctk.CTkLabel(
    master=app,
    text='Укажите где расположить "C:\\sandbox\\output"',
    font=("Arial", 14, "bold"),
    text_color="#f8b015"
)
output_folder_label.place(x=20, y=220)

# Текст прогресс бара
progress_label = ctk.CTkLabel(
    master=app,
    text="0%",
    font=("Segoe UI", 12),
    text_color="#00a82a",
)
progress_label.place(x=700, y=180)

# Текст вывода результата
log_label = ctk.CTkLabel(
    master=app,
    text="Проверка расположение папок...",
    font=("Arial", 16, "bold"),
    text_color="#ffdd95"
)
log_label.place(x=20, y=320)

# Поле указания папки сортировки
folder_entry = ctk.CTkEntry(
    master=app,
    placeholder_text="Путь папки сортировки...",
    width=360,
    height=30,
    border_width=2,
    corner_radius=10
)
folder_entry.place(x=20, y=160)

# Поле указания папки вывода
output_folder_entry = ctk.CTkEntry(
    master=app,
    placeholder_text="Путь папки расположения...",
    width=360,
    height=30,
    border_width=2,
    corner_radius=10
)
output_folder_entry.place(x=20, y=260)

# Кнопка старта
start_button = ctk.CTkButton(
    master=app,
    text="Начать сортировку",
    width=120,
    height=32,
    border_width=0,
    corner_radius=8,
    hover=True,
    command=start_sort
)
start_button.place(x=20, y=500)

# Кнокпи обзора
browse_from_button = ctk.CTkButton(app, text="...", width=40, command=browse_from)
browse_from_button.place(x=390, y=160)
browse_to_button = ctk.CTkButton(app, text="...", width=40, command=browse_to)
browse_to_button.place(x=390, y=260)

# Прогресс бар
progress = ctk.CTkProgressBar(
    master=app,
    width=250,
    height=18,
    corner_radius=9,
    progress_color="#00a82a",
    fg_color="#2a2a2a"
)
progress.set(0)
progress.place(x=500, y=160)

app.mainloop()