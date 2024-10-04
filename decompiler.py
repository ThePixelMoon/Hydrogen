#- decompiler.py -#
import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar, Menu, filedialog, messagebox
from eft import Theme
from settings import Settings
from utils import *
import os, json

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

            self.bold = self.settings.get_bold_text()
            self.italic = self.settings.get_italic_text()
            
            self.font_weight = "bold" if self.bold else "normal"
            self.font_slant = "italic" if self.italic else "roman"

            self.font_size = 10
            self.min_font_size = 8
            self.max_font_size = 30
            
            self.language = "en" # default
            self.translations = self.load_translations()

            self.output_text = Text(self.decompiler_window, wrap=tk.WORD)
            self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.output_text.configure(font=("Courier New", self.font_size, self.font_weight, self.font_slant), bg=self.theme.get_property("output_color"), fg=self.theme.get_property("output_text_color"))
            self.scrollbar = Scrollbar(self.decompiler_window, command=self.output_text.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.output_text.config(yscrollcommand=self.scrollbar.set)
            
            if os.name == "nt":  # windows
                self.decompiler_window.iconbitmap("assets/hydrogen_light.ico")
                utils.dark_title_bar(self.decompiler_window)
            else:
                self.decompiler_window.iconbitmap("assets/hydrogen.ico")

            self.create_menu()
            self.master.bind("<Control-MouseWheel>", self.resize_font)

    def load_translations(self):
        try:
            with open(f"translations/{self.language}.json", "r", encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def translate(self, key):
        return self.translations.get(self.language, {}).get(key, key)

    def resize_font(self, event):
        if event.delta > 0 and self.font_size < self.max_font_size:
            self.font_size += 1
        elif event.delta < 0 and self.font_size > self.min_font_size:
            self.font_size -= 1
        self.output_text.configure(font=("Courier New", self.font_size, self.font_weight, self.font_slant))

        self.output_text.tag_configure('chunk', font=("Courier New", self.font_size, self.font_weight, self.font_slant))

    def create_menu(self):
        menu_bar = Menu(self.decompiler_window)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label=self.translate("save_output"), command=self.save_output)
        file_menu.add_separator()
        file_menu.add_command(label=self.translate("exit"), command=self.decompiler_window.destroy)
        menu_bar.add_cascade(label=self.translate("file"), menu=file_menu)
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
                        c_code.append(f"if ({dest} == {src}) {{ /* {self.translate("not_implemented")} */ }}")
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
                        c_code.append(f"// {self.translate("no_operation")}")
                    case "test" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"if ({dest} & {src}) {{ /* {self.translate("not_implemented")} */ }}")
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
                    case "mulx" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} *= {src};")
                    case "divu" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} = ({dest} / {src});")
                    case "mod" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} %= {src};")
                    case "callx" if len(tokens) >= 2:
                        function_name = tokens[1]
                        params = ', '.join(tokens[2:])
                        c_code.append(f"{function_name}({params});")
                    case "nopx":
                        c_code.append("// no operation")
                    case "syscall" if len(tokens) >= 2:
                        syscall_number = tokens[1]
                        c_code.append(f"syscall({syscall_number});")
                    case "wait" if len(tokens) >= 2:
                        condition = tokens[1]
                        c_code.append(f"while (!({condition})) {{}}")
                    case "exit":
                        c_code.append("exit(0);")
                    case "jmpc" if len(tokens) >= 3:
                        condition, target = tokens[1:3]
                        c_code.append(f"if ({condition}) goto {target};")
                    case "load" if len(tokens) >= 3:
                        dest, address = tokens[1:3]
                        c_code.append(f"{dest} = load_memory({address});")
                    case "store" if len(tokens) >= 3:
                        src, address = tokens[1:3]
                        c_code.append(f"store_memory({address}, {src});")
                    case "movzx" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} = (unsigned int){src};")
                    case "movsx" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} = (int){src};")
                    case "clc":
                        c_code.append("carry_flag = 0;")
                    case "stc":
                        c_code.append("carry_flag = 1;")
                    case "tst" if len(tokens) >= 2:
                        src = tokens[1]
                        c_code.append(f"if ({src}) {{}}")
                    case "rol" if len(tokens) >= 3:
                        dest, count = tokens[1:3]
                        c_code.append(f"{dest} = ({dest} << {count}) | ({dest} >> (sizeof({dest}) * 8 - {count}));")
                    case "ror" if len(tokens) >= 3:
                        dest, count = tokens[1:3]
                        c_code.append(f"{dest} = ({dest} >> {count}) | ({dest} << (sizeof({dest}) * 8 - {count}));")
                    case "pushf":
                        c_code.append("push_flags();")
                    case "popf":
                        c_code.append("pop_flags();")
                    case "int" if len(tokens) >= 2:
                        interrupt_number = tokens[1]
                        c_code.append(f"interrupt({interrupt_number});")
                    case "hlt":
                        c_code.append("halt();")
                    case "callr" if len(tokens) >= 2:
                        label = tokens[1]
                        c_code.append(f"goto {label};")
                    case "rep" if len(tokens) >= 2:
                        instruction = tokens[1]
                        c_code.append(f"while (condition) {{ {instruction}; }}")
                    case "int3":
                        c_code.append("asm volatile(\"int $3\");")
                    case "nop2":
                        c_code.append("asm volatile(\"nop\");")
                    case "jmpq" if len(tokens) >= 2:
                        target = tokens[1]
                        c_code.append(f"goto {target};")
                    case "xchg" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{{ {dest} = {src}; {src} = {dest}; }}")
                    case "incx" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest}++;")
                    case "decx" if len(tokens) >= 2:
                        dest = tokens[1]
                        c_code.append(f"{dest}--;");
                    case "lea" if len(tokens) >= 3:
                        dest, src = tokens[1:3]
                        c_code.append(f"{dest} = &{src};")
                    case "shlx" if len(tokens) >= 3:
                        dest, count = tokens[1:3]
                        c_code.append(f"{dest} <<= {count};")
                    case "shrx" if len(tokens) >= 3:
                        dest, count = tokens[1:3]
                        c_code.append(f"{dest} >>= {count};")
                    case _:
                        continue

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "\n".join(c_code))
        self.output_text.config(state=tk.DISABLED)

    def save_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[(self.translate("text_files"), "*.txt"), (self.translate("all_files"), "*.*")],
            title=self.translate("save_output")
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    output = self.output_text.get("1.0", tk.END)
                    file.write(output)
                messagebox.showinfo(self.translate("success"), f"{self.translate("output_saved")} {file_path}.")
            except Exception as e:
                messagebox.showerror(self.translate("error"), f"{self.translate("failed_output")} {str(e)}")
