#- settings.py -#
import json, os, sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from eft import Theme
from utils import *

class Settings:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.settings = {
            "language": "en",
            "theme": "themes/default.eft",
            "font_size": 12,
            "bold_text": False,
            "italic_text": False
        }
        self.load_settings()
        
        self.theme = Theme.EFT_Theme(self.get_theme())
        self.language = self.get_language()
        self.translations = self.load_translations()
        
        self.style = ttk.Style()
        self.style.layout("TNotebook", [])
        self.style.configure("TNotebook", borderwidth=0, tabmargins=0, relief="solid", background=self.theme.get_property("bg_color")) 
        
    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_theme(self):
        return self.settings["theme"]

    def set_theme(self, theme_path):
        self.settings["theme"] = theme_path
        self.save_settings()

    def get_font_size(self):
        return self.settings.get("font_size", 12)

    def set_font_size(self, size):
        self.settings["font_size"] = size
        self.save_settings()

    def get_bold_text(self):
        return self.settings.get("bold_text", False)

    def set_bold_text(self, bold):
        self.settings["bold_text"] = bold
        self.save_settings()

    def get_italic_text(self):
        return self.settings.get("italic_text", False)

    def set_italic_text(self, italic):
        self.settings["italic_text"] = italic
        self.save_settings()

    def get_language(self):
        return self.settings.get("language", "en")

    def set_language(self, lang):
        self.settings["language"] = lang
        self.save_settings()

    def load_translations(self):
        try:
            with open(f"translations/{self.language}.json", "r", encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def translate(self, key):
        return self.translations.get(self.language, {}).get(key, key)

    def open_window(self, master, object):
        self.settings_window = tk.Toplevel(master)
        self.settings_window.title(self.translate("settings"))
        self.settings_window.geometry("400x300")
        self.settings_window.configure(bg=self.theme.get_property("bg_color"))
        self.settings_window.iconbitmap("assets/hydrogen.ico")

        self.notebook = ttk.Notebook(self.settings_window)
        self.notebook.pack(expand=True, fill='both')

        self.theme_frame = tk.Frame(self.notebook)
        self.general_frame = tk.Frame(self.notebook)

        self.notebook.add(self.general_frame, text=self.translate("general"))
        self.notebook.add(self.theme_frame, text=self.translate("theme"))

        self.create_general_tab(self.general_frame, object)
        self.create_theme_tab(self.theme_frame, object)
        
        self.save_button = tk.Button(self.settings_window, text="Save", command=lambda: self.save_settings_ui(object))
        self.save_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)
        self.save_button.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))

        if os.name == "nt":  # windows
            self.settings_window.iconbitmap("assets/hydrogen_light.ico")
            utils.dark_title_bar(self.settings_window)
        else:
            self.settings_window.iconbitmap("assets/hydrogen.ico")

        #self.notebook.configure(bg=self.theme.get_property("bg_color"))

    def create_theme_tab(self, frame, object):
        frame.configure(bg=self.theme.get_property("bg_color"))

        theme_selection_frame = tk.Frame(frame, bg=self.theme.get_property("bg_color"))
        theme_selection_frame.pack(pady=10, anchor='w')

        self.theme_label = tk.Label(theme_selection_frame, text=self.translate("select_theme"))
        self.theme_label.pack(side=tk.LEFT)
        self.theme_label.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))

        self.theme_entry = tk.Entry(theme_selection_frame)
        self.theme_entry.pack(side=tk.LEFT, padx=5)
        self.theme_entry.insert(0, os.path.basename(self.get_theme()))
        self.theme_entry.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))

        self.browse_button = tk.Button(theme_selection_frame, text=self.translate("browse"), command=self.browse_theme)
        self.browse_button.pack(side=tk.LEFT, padx=5)
        self.browse_button.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))

        self.style.configure("TNotebook", borderwidth=0, tabmargins=0, relief="solid", background=self.theme.get_property("bg_color")) 

    def on_language_change(self, event):
        self.set_language(self.language_var.get())
        messagebox.showinfo(self.translate("settings"), self.translate("language_changed"))
        self.restart_application()
        
    def restart_application(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def get_languages(self):
        translations_dir = 'translations/'
        languages = [f[:-5] for f in os.listdir(translations_dir) if f.endswith('.json')]
        return languages

    def create_general_tab(self, frame, object):
        frame.configure(bg=self.theme.get_property("bg_color"))

        language_label = tk.Label(frame, text=self.translate("language"), bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))
        language_label.pack(anchor='w', padx=10, pady=5)

        self.language_var = tk.StringVar(value=self.get_language())
        self.language_combobox = ttk.Combobox(frame, textvariable=self.language_var, values=self.get_languages(), state="readonly")
        self.language_combobox.set(self.language_var.get())
        self.language_combobox.pack(anchor='w', padx=10, pady=5)
        self.language_combobox.bind("<<ComboboxSelected>>", self.on_language_change)
        
        font_size_label = tk.Label(frame, text="Font Size:", bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))
        font_size_label.pack(anchor='w', padx=10, pady=5)

        self.font_size_spinbox = tk.Spinbox(frame, from_=10, to=72, width=5)
        self.font_size_spinbox.pack(anchor='w', padx=10)
        self.font_size_spinbox.delete(0, tk.END)
        self.font_size_spinbox.insert(0, self.get_font_size())
        
        self.bold_text_var = tk.BooleanVar(value=self.get_bold_text())
        bold_checkbox = tk.Checkbutton(frame, text=self.translate("bold"), var=self.bold_text_var, bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))
        bold_checkbox.pack(anchor='w', padx=10)

        self.italic_text_var = tk.BooleanVar(value=self.get_italic_text())
        italic_checkbox = tk.Checkbutton(frame, text=self.translate("italic"), var=self.italic_text_var, bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))
        italic_checkbox.pack(anchor='w', padx=10)

    def browse_theme(self):
        theme_path = filedialog.askopenfilename(title=self.translate("theme_file"), 
                                                 filetypes=[(f".EFT {self.translate("files")}", "*.eft")])
        if theme_path:
            self.theme_entry.delete(0, tk.END)
            self.theme_entry.insert(0, theme_path)

    def save_settings_ui(self, object):
        theme_path = self.theme_entry.get()
        if os.path.exists(theme_path):
            self.set_theme(theme_path)
            self.theme = Theme.EFT_Theme(self.get_theme())
            
            object.master.configure(bg=self.theme.get_property("bg_color"))
            object.output_text.tag_configure('function', foreground=self.theme.get_property("function"))
            object.output_text.tag_configure('builtin', foreground=self.theme.get_property("builtin"))
            object.output_text.tag_configure('error', foreground=self.theme.get_property("error"))
            object.output_text.tag_configure('punctuation', foreground=self.theme.get_property("punctuation"))
            object.output_text.tag_configure('address', foreground=self.theme.get_property("address"))
            object.output_text.tag_configure('chunk', foreground=self.theme.get_property("chunk"))
            object.output_text.tag_configure('highlight', background=self.theme.get_property("highlight"))
            object.output_text.configure(bg=self.theme.get_property("output_color"))
            object.output_text.configure(fg=self.theme.get_property("output_text_color")) 
            object.status_bar.configure(fg=self.theme.get_property("status_bar_text_color"), bg=self.theme.get_property("status_bar_color"))
            
            self.theme_label.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))
            self.theme_entry.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))
            self.settings_window.configure(bg=self.theme.get_property("bg_color"))
            self.save_button.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))
            self.browse_button.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))
            self.theme_frame.configure(bg=self.theme.get_property("bg_color"))
            self.general_frame.configure(bg=self.theme.get_property("bg_color"))

            self.style.layout("TNotebook", [])
            self.style.configure("TNotebook", borderwidth=0, tabmargins=0, relief="solid", background=self.theme.get_property("bg_color")) 
            self.style.configure("Vertical.TScrollbar", background=self.theme.get_property("scrollbar_color"))

        
        font_size = int(self.font_size_spinbox.get())
        self.set_font_size(font_size)

        bold = self.bold_text_var.get()
        italic = self.italic_text_var.get()

        font_weight = "bold" if bold else "normal"
        font_slant = "italic" if italic else "roman"
        
        object.font_size = font_size
        object.output_text.configure(font=("Courier New", font_size, font_weight, font_slant))
        
        messagebox.showinfo(self.translate("settings"), self.translate("settings_success"))