import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import struct
import os
import sys
# Helper functions for different conversions
def to_binary(n): return bin(n)[2:]
def to_octal(n): return oct(n)[2:]
def to_hexadecimal(n): return hex(n)[2:]
def to_base(n, base): return format(n, f'0{base}').upper()
def to_roman(n): return int_to_roman(n)  # Helper function for Roman numerals
def to_ieee_754(n): return format_float_ieee_754(n)

def from_binary(s): return int(s, 2)
def from_octal(s): return int(s, 8)
def from_hexadecimal(s): return int(s, 16)
def from_base(s, base): return int(s, base)
def from_roman(s): return roman_to_int(s)  # Helper function for Roman numerals
def from_ieee_754(s): return ieee_754_to_float(s)

# Conversion functions for Roman numerals
def int_to_roman(n):
    roman_numerals = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
                      (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    result = ''
    for value, symbol in roman_numerals:
        while n >= value:
            result += symbol
            n -= value
    return result

def roman_to_int(s):
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    for char in reversed(s):
        value = roman_values[char]
        if value >= prev_value:
            total += value
        else:
            total -= value
        prev_value = value
    return total

# Conversion functions for IEEE 754 floating-point representation
def format_float_ieee_754(f):
    return ''.join(f'{c:08b}' for c in struct.pack('>f', f))

def ieee_754_to_float(binary_str):
    return struct.unpack('>f', int(binary_str, 2).to_bytes(4, 'big'))[0]

# Dictionary for format conversion functions
CONVERSIONS = {
    'Binary': (to_binary, from_binary),
    'Octal': (to_octal, from_octal),
    'Decimal': (str, int),
    'Hexadecimal': (to_hexadecimal, from_hexadecimal),
    'Base-3': (lambda n: to_base(n, 3), lambda s: from_base(s, 3)),
    'Base-5': (lambda n: to_base(n, 5), lambda s: from_base(s, 5)),
    'Base-12': (lambda n: to_base(n, 12), lambda s: from_base(s, 12)),
    'Base-20': (lambda n: to_base(n, 20), lambda s: from_base(s, 20)),
    'Base-26': (lambda n: to_base(n, 26), lambda s: from_base(s, 26)),
    'Base-32': (lambda n: to_base(n, 32), lambda s: from_base(s, 32)),
    'Base-36': (lambda n: to_base(n, 36), lambda s: from_base(s, 36)),
    'Roman': (to_roman, from_roman),
    'IEEE 754': (to_ieee_754, from_ieee_754)
}

# Tkinter GUI Setup
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores data there
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ConversionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Format Converter")
        self.root.geometry("600x400")

        # Load and set the background image
        self.background_image = Image.open(resource_path("img.jpg"))  # Load the image using resource_path
        self.background_image = self.background_image.resize((600, 400), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create a canvas to hold the background image
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.grid(row=0, column=0, columnspan=3, rowspan=6)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)

        # Input field
        self.input_label = ttk.Label(root, text="Input Number:", background='#707070', foreground='black')
        self.input_label.place(x=20, y=20)
        self.input_entry = tk.Entry(root, font=('Arial', 10), width=25, relief="solid", bg='#707070', fg='white')
        self.input_entry.place(x=150, y=20)

        # Paste button for input field
        self.paste_button = ttk.Button(root, text="Paste", command=self.paste_input)
        self.paste_button.place(x=470, y=20)

        # Input format dropdown
        self.input_format_label = ttk.Label(root, text="Input Format:", background='#707070', foreground='black')
        self.input_format_label.place(x=20, y=80)
        self.input_format_var = tk.StringVar(value="Decimal")
        self.input_format_dropdown = ttk.Combobox(root, textvariable=self.input_format_var, values=list(CONVERSIONS.keys()),background='#707070', foreground='red')
        self.input_format_dropdown.place(x=150, y=80)

        # Output format dropdown
        self.output_format_label = ttk.Label(root, text="Output Format:", background='#707070', foreground='black')
        self.output_format_label.place(x=20, y=140)
        self.output_format_var = tk.StringVar(value="Binary")
        self.output_format_dropdown = ttk.Combobox(root, textvariable=self.output_format_var, values=list(CONVERSIONS.keys()),background='#707070', foreground='red')
        self.output_format_dropdown.place(x=150, y=140)

        # Convert button
        self.convert_button = ttk.Button(root, text="Convert", command=self.convert)
        self.convert_button.place(x=260, y=200)

        # Result field
        self.result_label = ttk.Label(root, text="Converted Value:", background='#707070', foreground='black')
        self.result_label.place(x=20, y=260)
        self.result_value = tk.StringVar()
        self.result_entry = tk.Entry(root, textvariable=self.result_value, state='readonly', width=25, relief="solid", bg='#707070', fg='black')
        self.result_entry.place(x=150, y=260)

        # Copy button for result field
        self.copy_button = ttk.Button(root, text="Copy", command=self.copy_result)
        self.copy_button.place(x=470, y=260)

    # Method to handle conversion
    def convert(self):
        input_value = self.input_entry.get()
        input_format = self.input_format_var.get()
        output_format = self.output_format_var.get()

        try:
            # Convert input to decimal
            to_decimal_func = CONVERSIONS[input_format][1]
            decimal_value = to_decimal_func(input_value)

            # Convert decimal to output format
            to_output_func = CONVERSIONS[output_format][0]
            output_value = to_output_func(decimal_value)

            # Display result
            self.result_value.set(output_value)

        except ValueError:
            self.result_value.set("Error: Invalid Input")

    # Method to copy result to clipboard
    def copy_result(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_value.get())

    # Method to paste clipboard content into input field
    def paste_input(self):
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, self.root.clipboard_get())

# Run the app
root = tk.Tk()
app = ConversionApp(root)
root.mainloop()
