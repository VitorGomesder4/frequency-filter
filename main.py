import tkinter as tk

window = tk.Tk()

largura = window.winfo_screenwidth() / 2
altura = window.winfo_screenheight() / 2

window.config(height=altura, width=largura)
window.state("zoomed")


window.mainloop()