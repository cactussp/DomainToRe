from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
import re
import pyperclip


class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


ctk.set_appearance_mode("dark")


# ctk.set_default_color_theme("blue")

def copy_to_clipboard(text):
    pyperclip.copy(text)


def get_file_content(event):
    try:
        # Используем регулярное выражение для обработки нескольких файлов
        pattern = r'\{[^\}]*\}|\S+'
        file_paths = re.findall(pattern, event.data)
        file_paths = [path.strip('{}') for path in file_paths]

        # Очистка фрейма для новых результатов
        for widget in result_frame.winfo_children():
            widget.destroy()



        # Создаем фрейм для таблицы
        table_frame = ctk.CTkScrollableFrame(result_frame,width=1100,)
        table_frame.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)
        # Создаем заголовки
        headers = "Домен", "Копировать домен", "Regex", "Копировать regex"
        for i, header in enumerate(headers):
            ctk.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=5)
        row = 1  # Начинаем с первой строки после заголовков
        unique_domains = list()
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                # Поиск доменных имен
                domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.){1,5}[a-zA-Z]{2,6}\b'
                unique_domains.extend(re.findall(domain_pattern, content))

        if unique_domains:
            for domain in unique_domains:
                # Формируем регулярное выражение
                escaped_domain = re.escape(domain)
                regex_pattern = f"(^|\\.)(?:.*\\.)?{escaped_domain}$"

                # Создаем строку таблицы
                ctk.CTkLabel(table_frame, text=domain, width=200).grid(row=row, column=0, padx=10, pady=5,
                                                                       sticky=ctk.W)
                ctk.CTkButton(table_frame, text="Копировать", width=100,
                              command=lambda d=domain: copy_to_clipboard(d)).grid(row=row, column=1, padx=10,
                                                                                  pady=5)
                ctk.CTkLabel(table_frame, text=regex_pattern, width=300).grid(row=row, column=2, padx=10, pady=5,
                                                                              sticky=ctk.W)
                ctk.CTkButton(table_frame, text="Копировать", width=100,
                              command=lambda r=regex_pattern: copy_to_clipboard(r)).grid(row=row, column=3, padx=10,
                                                                                         pady=5)

                row += 1  # Переходим к следующей строке
        else:
            ctk.CTkLabel(table_frame, text="Доменные имена не найдены в файле").grid(row=row, column=0,
                                                                                     columnspan=4, padx=10, pady=5)
            row += 1
    except Exception as e:
        ctk.CTkLabel(result_frame, text=f"Ошибка при чтении файла: {str(e)}").pack(pady=10)


root = Tk()
root.resizable(width=False, height=True)
root.title("Домен Finder")
result_frame = ctk.CTkFrame(root)
result_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

text_widget = ctk.CTkLabel(result_frame, width=1100, height=500, text="Переместите файл с доменами сюда",
                           fg_color="transparent")
text_widget.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

text_widget.drop_target_register(DND_ALL)
text_widget.dnd_bind("<<Drop>>", get_file_content)

root.mainloop()
