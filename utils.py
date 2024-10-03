#- utils.py -#
import ctypes as ct
import os

class utils:
    # https://github.com/alijafari79/Tkinter_dark_Title_bar
    def dark_title_bar(window):
        if os.name == "nt":  # windows
            window.update()
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ct.windll.user32.GetParent
            hwnd = get_parent(window.winfo_id())
            rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
            value = 2
            value = ct.c_int(value)
            set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))
