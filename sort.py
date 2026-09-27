import os, shutil

categories = {
    "Документы": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".fb2", ".epub"],
    "Программы": [".exe", ".msi", ".apk", ".bat", ".cmd"],
    "Изображения": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico"],
    "Видео": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Аудио": [".mp3", ".wav", ".flac", ".ogg"],
    "Архивы": [".zip", ".rar", ".7z", ".tar", ".gz"]
}

def sort_my_files(folder_from, folder_to, log_label, progress_bar, progress_label):
    if not os.path.exists(folder_from):
        log_label.after(0, lambda: log_label.configure(text="Ошибка! Папка сортировки не существует", text_color="#FF6B6B"))
        return
    
    if not os.path.exists(folder_to):
        log_label.after(0, lambda: log_label.configure(text="Ошибка! Папка вывода не существует", text_color="#FF6B6B"))
        return
    
    if os.path.exists(folder_to) and os.path.exists(folder_from):
        log_label.after(0, lambda: log_label.configure(text="Обработка", text_color="#7BF0FF"))
        
    all_files = [f for f in os.listdir(folder_from) if os.path.isfile(os.path.join(folder_from, f))]
    total_files = len(all_files)
    
    if total_files == 0:
        log_label.after(0, lambda: log_label.configure(text="В папке нет файлов", text_color="#FFB86B"))
        return
    
    for index, item in enumerate(all_files, 1):
        item_path = os.path.join(folder_from, item)
        
        _, ext = os.path.splitext(item.lower())         
        found = False
        
        for folder_name, extensions in categories.items():
            if ext in extensions:
                final_folder = os.path.join(folder_to, folder_name)
                os.makedirs(final_folder, exist_ok=True)
                
                shutil.move(item_path, os.path.join(final_folder, item))
            
                found = True
                break
        
        if not found:
            other_folder = os.path.join(folder_to, "Другое")
            os.makedirs(other_folder, exist_ok=True)
            shutil.move(item_path, os.path.join(other_folder, item))

        current_progress = index / total_files
        
        progress_bar.after(0, lambda v=current_progress: progress_bar.set(v))
        progress_label.after(0, lambda v=current_progress: progress_label.configure(text=f"{int(v * 100)}%"))
        
    progress_bar.after(0, lambda: progress_bar.set(1.0))
    progress_label.after(0, lambda: progress_label.configure(text="100%"))
    log_label.after(0, lambda: log_label.configure(text="Сортировка успешно завершена", text_color="#20F755"))