#- settings.py -#
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from eft import Theme
from utils import *

class Settings:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.settings = {
            "theme": "themes/default.eft",
        }
        self.load_settings()
        
        self.theme = Theme.EFT_Theme(self.get_theme())
        
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

    def open_window(self, master, object):
        self.settings_window = tk.Toplevel(master)
        self.settings_window.title("Settings")
        self.settings_window.geometry("400x300")
        self.settings_window.configure(bg=self.theme.get_property("bg_color"))
        self.settings_window.iconbitmap("assets/hydrogen.ico")

        self.notebook = ttk.Notebook(self.settings_window)
        self.notebook.pack(expand=True, fill='both')

        self.theme_frame = tk.Frame(self.notebook)
        self.general_frame = tk.Frame(self.notebook)

        self.notebook.add(self.theme_frame, text="Theme")
        self.notebook.add(self.general_frame, text="General")

        self.create_theme_tab(self.theme_frame, object)
        self.create_general_tab(self.general_frame, object)
        
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

        self.theme_label = tk.Label(theme_selection_frame, text="Select Theme:")
        self.theme_label.pack(side=tk.LEFT)
        self.theme_label.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))

        self.theme_entry = tk.Entry(theme_selection_frame)
        self.theme_entry.pack(side=tk.LEFT, padx=5)
        self.theme_entry.insert(0, os.path.basename(self.get_theme()))
        self.theme_entry.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))

        self.browse_button = tk.Button(theme_selection_frame, text="Browse", command=self.browse_theme)
        self.browse_button.pack(side=tk.LEFT, padx=5)
        self.browse_button.configure(bg=self.theme.get_property("bg_color"), fg=self.theme.get_property("output_text_color"))

        self.style.configure("TNotebook", borderwidth=0, tabmargins=0, relief="solid", background=self.theme.get_property("bg_color")) 

    def create_general_tab(self, frame, object):
        frame.configure(bg=self.theme.get_property("bg_color"))

    def browse_theme(self):
        theme_path = filedialog.askopenfilename(title="Select Theme File", 
                                                 filetypes=[("EFT Files", "*.eft")])
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

            messagebox.showinfo("Settings", "Settings saved successfully!")
        else:
            messagebox.showerror("Error", "Invalid theme file path.")
