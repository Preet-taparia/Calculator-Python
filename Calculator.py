import tkinter as tk
from tkinter import scrolledtext
import math

class Calculator:
    def __init__(self, root):
        self.answer_variable = ""
        self.expression_label = None
        self.result_label = None
        self.history_text = None
        self.history = []
        self.root = root

    def create_widgets(self):
        self.create_expression_label()
        self.create_result_label()
        self.create_history_text()
        self.create_buttons()

    def create_expression_label(self):
        self.expression_label = self.create_label(self.root, font=('Arial', 25, 'bold'), height=2, width=20)
        self.expression_label.grid(row=0, column=0, columnspan=4, sticky="nsew")

    def create_result_label(self):
        self.result_label = self.create_label(self.root, font=('Arial', 25, 'bold'), height=2, width=20, fg='gray')
        self.result_label.grid(row=1, column=0, columnspan=4, sticky="nsew")

    def create_history_text(self):
        self.history_text = scrolledtext.ScrolledText(self.root, font=('Arial', 15), height=10, width=20, wrap=tk.WORD, state=tk.DISABLED)
        self.history_text.grid(row=0, column=4, rowspan=8, padx=10, pady=10, sticky="nsew")
        self.history_text.insert(tk.END, "History")

    def create_buttons(self):
        buttons = [
            'AC', '√', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.'
        ]

        buttons_list_traversal_counter = 0
        for i in range(2, 7):
            for j in range(4):
                if buttons_list_traversal_counter < len(buttons):
                    button_text = buttons[buttons_list_traversal_counter]
                    if button_text:
                        self.create_button(
                            row=i,
                            column=j,
                            text=button_text,
                            command=lambda txt=button_text: self.handle_button_click(txt),
                        )
                    buttons_list_traversal_counter += 1

        self.create_button(row=2, column=1, text="√", command=self.handle_square_root)
        self.create_button(row=2, column=0, text="AC", command=self.all_clear)
        self.create_button(row=6, column=3, text="=", command=self.evaluate_expression)
        self.create_button(row=6, column=2, text="⌫", command=self.backspace)
        self.create_button(row=6, column=1, text=".", command=self.handle_decimal_point)

    def create_label(self, parent, **kwargs):
        label = tk.Label(parent, **kwargs)
        return label

    def create_button(self, row, column, text, command):
        button = tk.Button(
            self.root,
            font=('Arial', 15, 'bold'),
            padx=16,
            pady=16,
            text=text,
            command=command,
            height=2,
            width=9
        )
        button.grid(row=row, column=column, sticky="nsew")

    def handle_button_click(self, entry):
        self.answer_variable += str(entry)
        self.expression_label['text'] = self.answer_variable
        self.clear_result_label()

    def handle_decimal_point(self):
        if "." not in self.answer_variable:
            self.answer_variable += "."
            self.expression_label['text'] = self.answer_variable
            self.clear_result_label()

    def backspace(self):
        self.answer_variable = self.answer_variable[:-1]
        self.expression_label['text'] = self.answer_variable
        self.clear_result_label()

    def evaluate_expression(self):
        expression = self.answer_variable
        try:
            result = eval(expression)
            self.answer_variable = str(result)
            self.expression_label['text'] = self.answer_variable
            self.result_label['text'] = str(result)
            history_entry = f"{expression} = {result}\n"
            self.history.append(history_entry)
            self.update_history_text()
        except ZeroDivisionError:
            self.clear_answer_entry_label()
            self.result_label['text'] = "Division by Zero"
        except (ValueError, SyntaxError, TypeError):
            self.clear_answer_entry_label()
            self.result_label['text'] = "Invalid Expression"

    def update_history_text(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, "History\n")
        for entry in self.history:
            self.history_text.insert(tk.END, entry)
        self.history_text.config(state=tk.DISABLED)

    def clear_answer_entry_label(self):
        self.answer_variable = ""
        self.expression_label['text'] = ""

    def handle_square_root(self):
        try:
            value = eval(str(self.answer_variable))
            if value < 0:
                self.clear_answer_entry_label()
                self.result_label['text'] = "Negative Number Input"
            else:
                sqrt_answer = math.sqrt(value)
                self.answer_variable = str(sqrt_answer)
                self.expression_label['text'] = self.answer_variable
                self.result_label['text'] = str(sqrt_answer)
                history_entry = f"√({value}) = {sqrt_answer}\n"
                self.history.append(history_entry)
                self.update_history_text()
        except (ValueError, SyntaxError, TypeError):
            self.clear_answer_entry_label()
            self.result_label['text'] = "Invalid Input"

    def all_clear(self):
        self.clear_answer_entry_label()
        self.clear_result_label()
        self.clear_history()

    def clear_result_label(self):
        self.result_label['text'] = ""

    def clear_history(self):
        self.history = []
        self.update_history_text()

def main():
    root = tk.Tk()
    root.title('Calculator App')

    calculator = Calculator(root)
    calculator.create_widgets()

    root.mainloop()

if __name__ == "__main__":
    main()
