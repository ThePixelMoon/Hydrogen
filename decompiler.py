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

                match tokens[0]:
                    case "mov" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} = {src};")
                    case "add" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} += {src};")
                    case "sub" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} -= {src};")
                    case "mul" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} *= {src};")
                    case "div" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} /= {src};")
                    case "jmp" if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"goto {target};")
                    case "jz" if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"if (condition == 0) goto {target};")
                    case "jnz" if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"if (condition != 0) goto {target};")
                    case "cmp" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"if ({dest} == {src}) {{ /* not implemented */ }}")
                    case "call" if len(tokens) >= 2:
                        function_name = tokens[1]
                        c_code.append(f"{function_name}();")
                    case "and" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} &= {src};")
                    case "or" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} |= {src};")
                    case "xor" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} ^= {src};")
                    case "push" if len(tokens) >= 2:
                        src = tokens[1]
                        c_code.append(f"stack_push({src});")
                    case "pop" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = stack_pop();")
                    case "ret":
                        c_code.append("return;")
                    case "inc" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest}++;")
                    case "dec" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest}--;")
                    case "nop":
                        c_code.append("// no operation")
                    case "test" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"if ({dest} & {src}) {{ /* not implemented */ }}")
                    case "shl" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} <<= {src};")
                    case "shr" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} >>= {src};")
                    case "not" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = ~{dest};")
                    case "jmpnz" if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"if (condition != 0) goto {target};")
                    case "jmpz" if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"if (condition == 0) goto {target};")
                    case "sete" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition == 0) ? 1 : 0;")
                    case "setne" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition != 0) ? 1 : 0;")
                    case "setg" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition > 0) ? 1 : 0;")
                    case "setl" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition < 0) ? 1 : 0;")
                    case "setge" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition >= 0) ? 1 : 0;")
                    case "setle" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest} = (condition <= 0) ? 1 : 0;")
                    case _:
                        continue

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
