#- main.py -#
from disassembler import Disassembler, tk

if __name__ == "__main__":
    root = tk.Tk()
    app = Disassembler(root)
    root.mainloop()
