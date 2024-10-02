#- disassembler.py -#
import tkinter as tk
from tkinter import filedialog, Scrollbar,\
                    Frame, Text, Menu, simpledialog,\
                    messagebox
from capstone import *
from capstone.x86 import *
from eft import Theme
import pefile, find_utils, threading
from pygments.lexers import NasmLexer
from pygments.token import Token
from settings import Settings

class Disassembler:
    def __init__(self, master):
        self.settings = Settings()
        self.theme = Theme.EFT_Theme(self.settings.get_theme())
        
        self.master = master
        self.master.title("Codename Hydrogen")
        self.master.geometry("600x400")
        self.master.configure(bg=self.theme.get_property("bg_color"))
                
        self.font_size = 10
        self.min_font_size = 8
        self.max_font_size = 30
        
        self.is_disassembling = False

        self.create_menu()
        self.create_output_area()
        self.create_status_bar()

        self.output_text.tag_configure('function', foreground=self.theme.get_property("function"))
        self.output_text.tag_configure('builtin', foreground=self.theme.get_property("builtin"))
        self.output_text.tag_configure('error', foreground=self.theme.get_property("error"))
        self.output_text.tag_configure('punctuation', foreground=self.theme.get_property("punctuation"))
        self.output_text.tag_configure('address', foreground=self.theme.get_property("address"))
        self.output_text.tag_configure('chunk', foreground=self.theme.get_property("chunk"))
        self.output_text.tag_configure('highlight', background=self.theme.get_property("highlight"))

        self.output_text.configure(font=("Courier New", self.font_size))

        self.master.bind("<Control-MouseWheel>", self.resize_font)

    def create_menu(self):
        self.menu_bar = Menu(self.master)

        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Load", command=self.open_file)
        file_menu.add_command(label="Save Output", command=self.save_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        
        find_menu = Menu(self.menu_bar, tearoff=0)
        find_menu.add_command(label="Find String", command=self.find_string)
        find_menu.add_command(label="Find Address", command=self.find_address)
        
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Change Theme", command=self.change_theme)
        file_menu.add_separator()
        help_menu.add_command(label="About", command=self.about)
        
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Find", menu=find_menu)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        self.master.config(menu=self.menu_bar)

    def create_output_area(self):
        self.output_frame = Frame(self.master)
        self.output_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(self.output_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = Text(self.output_frame, wrap=tk.WORD, width=80, height=20, yscrollcommand=self.scrollbar.set, bg="#ffffff", fg="#000000", font=("Courier New", self.font_size))
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output_text.configure(state=tk.DISABLED, bg=self.theme.get_property("output_color"), fg=self.theme.get_property("output_text_color"))

        self.scrollbar.config(command=self.output_text.yview)
        
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def about(self):
        messagebox.showinfo("Hydrogen", "Made with ♥ by YourLocalMoon")
        return

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.master, textvariable=self.status_var, bg=self.theme.get_property("status_bar_color"), anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_var.set("Ready")

    def get_arch_and_mode(self, pe_file):
        if pe_file.FILE_HEADER.Machine == 0x8664:
            return CS_ARCH_X86, CS_MODE_64
        elif pe_file.FILE_HEADER.Machine == 0x14c:
            return CS_ARCH_X86, CS_MODE_32
        else:
            return None, None

    def get_main_code_section(self, sections, base_of_code):
        addresses = [section.VirtualAddress for section in sections]
        if base_of_code in addresses:
            return sections[addresses.index(base_of_code)]
        else:
            addresses.append(base_of_code)
            addresses.sort()
            if addresses.index(base_of_code) != 0:
                return sections[addresses.index(base_of_code) - 1]
            return None

    def fine_disassemble(self, file=None, arch=None, mode=None):
        if file is None:
            messagebox.showinfo("Error", "BETCH PROVIDE A FILE!!")
            return
        
        main_code = self.get_main_code_section(file.sections, file.OPTIONAL_HEADER.BaseOfCode)
        md = Cs(arch, mode)
        md.detail = True
        md.skipdata = True
        begin = main_code.PointerToRawData
        end = begin + main_code.SizeOfRawData
        disassembly_output = []

        total_size = end - begin
        chunk_size = 0x10000  # 64KB
        progress = 0

        while begin < end:
            data = file.get_memory_mapped_image()[begin:begin + chunk_size]
            for i in md.disasm(data, begin):
                disassembly_output.append(f"{i.address:x}: {i.mnemonic} {i.op_str}")
            begin += chunk_size
            progress = (begin - main_code.PointerToRawData) / total_size * 100

            self.master.after(0, self.update_progress, progress)

        return disassembly_output

    def update_progress(self, progress):
        self.status_var.set(f"Disassembling... {min(progress, 100):.2f}% complete")

    def change_theme(self):
        theme_path = filedialog.askopenfilename(title="Select .eft file", filetypes=[("EFT Files", "*.eft")])
        if theme_path:
            self.theme = Theme.EFT_Theme(theme_path)
            self.update_ui_theme()
            self.settings.set_theme(theme_path)

    def update_ui_theme(self):
        self.master.configure(bg=self.theme.get_property("bg_color"))
        self.output_text.tag_configure('function', foreground=self.theme.get_property("function"))
        self.output_text.tag_configure('builtin', foreground=self.theme.get_property("builtin"))
        self.output_text.tag_configure('error', foreground=self.theme.get_property("error"))
        self.output_text.tag_configure('punctuation', foreground=self.theme.get_property("punctuation"))
        self.output_text.tag_configure('address', foreground=self.theme.get_property("address"))
        self.output_text.tag_configure('chunk', foreground=self.theme.get_property("chunk"))
        self.output_text.tag_configure('highlight', background=self.theme.get_property("highlight"))
        self.output_text.configure(bg=self.theme.get_property("output_color"))
        self.output_text.configure(fg=self.theme.get_property("output_text_color")) 

    def save_output(self):
        if self.is_disassembling:
            messagebox.showinfo("Info", "Please wait for the current disassembly to finish.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.output_text.get("1.0", tk.END))
            self.status_var.set(f"Saved output to: {file_path}")

    def highlight_code(self, code, chunk_size=20):
        lines = code.splitlines()
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)

        for i in range(0, len(lines), chunk_size):
            chunk = lines[i:i + chunk_size]
            self.output_text.insert(tk.END, "-------\n", 'chunk')
            for line in chunk:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    address, instruction = parts
                    self.output_text.insert(tk.END, f"{address.strip()}: ", 'address')
                    tokens = list(NasmLexer().get_tokens(instruction))
                    for token in tokens:
                        token_type, token_value = token
                        if token_type == Token.Name.Function:
                            self.output_text.insert(tk.END, token_value, 'function')
                        elif token_type == Token.Name.Builtin:
                            self.output_text.insert(tk.END, token_value, 'builtin')
                        elif token_type == Token.Error:
                            self.output_text.insert(tk.END, token_value, 'error')
                        elif token_type == Token.Text.Whitespace:
                            self.output_text.insert(tk.END, token_value)
                        elif token_type == Token.Punctuation:
                            self.output_text.insert(tk.END, token_value, 'punctuation')
                        else:
                            self.output_text.insert(tk.END, token_value)
                else:
                    self.output_text.insert(tk.END, line + "\n")

        self.output_text.configure(state=tk.DISABLED)

    def resize_font(self, event):
        if event.delta > 0 and self.font_size < self.max_font_size:
            self.font_size += 1
        elif event.delta < 0 and self.font_size > self.min_font_size:
            self.font_size -= 1
        self.output_text.configure(font=("Courier New", self.font_size))

        self.output_text.tag_configure('chunk', font=("Courier New", self.font_size))
       
    def open_file(self):
        if self.is_disassembling:
            messagebox.showinfo("Info", "Please wait for the current disassembly to finish.")
            return
        
        file_path = filedialog.askopenfilename(filetypes=[("Executable and DLL Files", "*.exe *.dll")])
        if file_path:
            self.status_var.set(f"Loading: {file_path}")
            threading.Thread(target=self.disassemble_in_background, args=(file_path,)).start()

    def disassemble_in_background(self, file_path):
        try:
            self.is_disassembling = True
            exe = pefile.PE(file_path)
            arch, mode = self.get_arch_and_mode(exe)
            disassembly = self.fine_disassemble(exe, arch, mode)
            disassembly_output = "\n".join(disassembly)
            self.highlight_code(disassembly_output)
            self.status_var.set(f"Loaded: {file_path}")
            self.is_disassembling = False
        except Exception as e:
            self.status_var.set(f"Error loading file: {e}")

    def find_string(self):
        search_string = simpledialog.askstring("Find String", "Enter string to search:")
        find_utils.find_string(self.output_text, search_string)

    def find_address(self):
        address = simpledialog.askstring("Find Address", "Enter address to find (in hex):")
        find_utils.find_address(self.output_text, address)
    