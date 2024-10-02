#- find_utils.py -#
import tkinter as tk
from tkinter import messagebox

def find_string(output_text, search_string):
    if search_string:
        output = output_text.get("1.0", tk.END)
        if search_string in output:
            start_index = output.index(search_string)
            end_index = start_index + len(search_string)
            start_line = output.count("\n", 0, start_index) + 1
            start_column = start_index - output.rfind("\n", 0, start_index) - 1

            output_text.tag_remove("highlight", "1.0", "end")
            output_text.tag_add("highlight", f"{start_line}.{start_column}", f"{start_line}.{end_index}")
            output_text.see(f"{start_line}.{start_column}")
            messagebox.showinfo("Search Result", f"Found '{search_string}' at line {start_line}.")
        else:
            messagebox.showinfo("Search Result", f"'{search_string}' not found.")

def find_address(output_text, address):
    if address:
        try:
            address = int(address, 16)
            output = output_text.get("1.0", tk.END)
            lines = output.splitlines()

            output_text.tag_remove("highlight", "1.0", "end")

            for line_number, line in enumerate(lines, start=1):
                if line.startswith(f"{address:x}:"):
                    output_text.see(f"{line_number}.0")

                    output_text.tag_add("highlight", f"{line_number}.0", f"{line_number}.end")
                    messagebox.showinfo("Search Result", f"Found at line {line_number}: {line.strip()}")
                    return

            messagebox.showinfo("Search Result", f"Address '{address:x}' not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid address format. Please enter a hex address.")