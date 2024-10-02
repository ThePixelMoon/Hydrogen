#- decompiler.py -#
import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar, Menu, filedialog, messagebox
from eft import Theme
from settings import Settings

class Decompiler:
    def __init__(self, master):
        self.master = master
        self.decompiler_window = None
        self.output_text = None

    def open_decompiler(self):
        if self.decompiler_window is None or not self.decompiler_window.winfo_exists():
            self.settings = Settings()
            self.theme = Theme.EFT_Theme(self.settings.get_theme())
            
            self.decompiler_window = Toplevel(self.master)
            self.decompiler_window.title("Decompiler")
            self.decompiler_window.geometry("600x400")
            self.decompiler_window.configure(bg=self.theme.get_property("bg_color"))

            self.output_text = Text(self.decompiler_window, wrap=tk.WORD)
            self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.output_text.configure(bg=self.theme.get_property("output_color"), fg=self.theme.get_property("output_text_color"))
            
            self.scrollbar = Scrollbar(self.decompiler_window, command=self.output_text.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.output_text.config(yscrollcommand=self.scrollbar.set)

            self.create_menu()

    def create_menu(self):
        menu_bar = Menu(self.decompiler_window)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save Output", command=self.save_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.decompiler_window.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.decompiler_window.config(menu=menu_bar)

    def decompile(self, disassembly):
        c_code = []

        for line in disassembly:
            parts = line.split(':')
            if len(parts) == 2:
                address, instruction = parts
                instruction = instruction.strip()

                tokens = instruction.split()
                if not tokens:
                    continue

                if "mov" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} = {src};")
                elif "add" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} += {src};")
                elif "sub" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} -= {src};")
                elif "mul" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} *= {src};")
                elif "div" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} /= {src};")
                elif "jmp" in instruction:
                    if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"goto {target};")
                elif "jz" in instruction:
                    if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"if (condition == 0) goto {target};")  
                elif "jnz" in instruction:
                    if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"if (condition != 0) goto {target};")
                elif "cmp" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"if ({dest} == {src}) {{ /* not implemented */ }}")
                elif "call" in instruction:
                    if len(tokens) >= 2:
                        function_name = tokens[1]
                        c_code.append(f"{function_name}();")
                elif "and" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} &= {src};")
                elif "or" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} |= {src};")
                elif "xor" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} ^= {src};")
                elif "push" in instruction:
                    if len(tokens) >= 2:
                        src = tokens[1]
                        c_code.append(f"stack_push({src});")
                elif "pop" in instruction:
                    if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = stack_pop();")
                elif "ret" in instruction:
                    c_code.append("return;")
                elif "inc" in instruction:
                    if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest}++;")
                elif "dec" in instruction:
                    if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest}--;")
                elif "nop" in instruction:
                    c_code.append("// No operation (ignored)")
                elif "test" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"if ({dest} & {src}) {{ /* not implemented */ }}")
                elif "shl" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} <<= {src};")
                elif "shr" in instruction:
                    if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} >>= {src};")
                elif "not" in instruction:
                    if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = ~{dest};")
                elif "jmpnz" in instruction:
                    if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"if (condition != 0) goto {target};")
                elif "jmpz" in instruction:
                    if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"if (condition == 0) goto {target};")
                elif "sete" in instruction:
                    if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition == 0) ? 1 : 0;")
                elif "setne" in instruction:
                    if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition != 0) ? 1 : 0;")
                elif "setg" in instruction:
                    if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition > 0) ? 1 : 0;")
                elif "setl" in instruction:
                    if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition < 0) ? 1 : 0;")
                elif "setge" in instruction:
                    if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition >= 0) ? 1 : 0;")
                elif "setle" in instruction:
                    if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition <= 0) ? 1 : 0;")

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "\n".join(c_code))
            self.output_text.config(state=tk.DISABLED)

    def save_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Output"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    output = self.output_text.get("1.0", tk.END)
                    file.write(output)
                messagebox.showinfo("Success", f"Output saved to {file_path}.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save output: {str(e)}")
