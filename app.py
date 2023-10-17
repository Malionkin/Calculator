import tkinter as tk
from decimal import Decimal
import re

def clean_input_string(input_string):
    parts = input_string.split('.')
    for part in parts:
        partss = part.split(' ')
        for i in range(1, len(partss)):
            if len(partss[i]) != 3:
                result_label.config(text="Неправильный формат вводимого числа")
                return

    cleaned_string = input_string.strip().replace(' ', '').replace(',', '.')
    if re.match(r'^[+-]?\d+(\.\d+)?$', cleaned_string):
        return cleaned_string
    return None

result = None

def format_result(result):
    formatted_result = f"{result:,.6f}".rstrip('0').rstrip('.').format().replace(',', ' ')
    return formatted_result

def calculate():
    global result
    num1_cleaned = clean_input_string(entry_num1.get())
    num2_cleaned = clean_input_string(entry_num2.get())

    if num1_cleaned is None or num2_cleaned is None:
        result_label.config(text="Ошибка при вводе чисел, возможно введены буквы либо формат неправильный")
        return

    try:
        num1 = Decimal(num1_cleaned)
        num2 = Decimal(num2_cleaned)
        operation = operation_var.get()

        if result is not None and ((num1 == result - num2) or (num1 == result + num2) or (num1 == result / num2) or (num1 == result * num2)):
            num1 = result
            entry_num1.delete(0, tk.END)
            entry_num1.insert(0, format_result(result))

        if operation == "Сложение":
            result = num1 + num2
        elif operation == "Вычитание":
            result = num1 - num2
        elif operation == "Умножение":
            result = num1 * num2
        elif operation == "Деление":
            if num2 != 0:
                result = num1 / num2
            else:
                result_label.config(text="Деление на ноль")
                return

        formatted_result = format_result(result)
        result_label.config(text=f"Результат: {formatted_result}")
    except Exception as e:
        result_label.config(text="Ошибка при вычислениях")

def copy_result():
    if result is not None:
        app.clipboard_clear()
        app.clipboard_append(format_result(result))
        app.update()
        result_label.config(text="Результат скопирован в буфер обмена")

# def paste_from_clipboard():
#     clipboard_data = app.clipboard_get()
#     if clipboard_data:
#         entry_num1.delete(0, tk.END)
#         entry_num1.insert(0, clipboard_data)

def copy_selected():
    # Get the currently selected text
    selected_text = app.clipboard_get()
    # Copy the selected text to the clipboard
    if selected_text:
        app.clipboard_clear()
        app.clipboard_append(selected_text)
        app.update()

def paste_selected(event=None):
    widget = app.focus_get()
    if isinstance(widget, tk.Entry):
        # Get the currently selected text from the clipboard
        selected_text = app.clipboard_get()
        selected_text = selected_text[:len(selected_text)/2]
        # Paste the selected text into the currently focused input field
        if selected_text:
            widget.insert(tk.INSERT, selected_text)
        app.update()



app = tk.Tk()
app.title("Калькулятор")
app.geometry("500x350")

student_info_label = tk.Label(app, text="ФИО: Малёнкин Яков Олегович\nКурс: 4\nГруппа: 4\nГод: 2023")
student_info_label.pack()

entry_num1 = tk.Entry(app, width=40)
entry_num1.pack()

entry_num2 = tk.Entry(app, width=40)
entry_num2.pack()

operation_var = tk.StringVar()
operation_var.set("Сложение")

addition_radio = tk.Radiobutton(app, text="Сложение", variable=operation_var, value="Сложение")
subtraction_radio = tk.Radiobutton(app, text="Вычитание", variable=operation_var, value="Вычитание")
multiplication_radio = tk.Radiobutton(app, text="Умножение", variable=operation_var, value="Умножение")
division_radio = tk.Radiobutton(app, text="Деление", variable=operation_var, value="Деление")

addition_radio.pack()
subtraction_radio.pack()
multiplication_radio.pack()
division_radio.pack()

calculate_button = tk.Button(app, text="Вычислить", command=calculate)
calculate_button.pack()

copy_button = tk.Button(app, text="Копировать результат", command=copy_result)
copy_button.pack()

result_label = tk.Label(app, text="Результат: ")
result_label.pack()

app.bind("<Control-v>", paste_selected)
app.bind("<Control-c>", lambda event=None: copy_selected())

app.mainloop()
