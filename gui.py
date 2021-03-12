from tkinter import *
#from tkinter import ttk


root = Tk()

# def command():
#    root.destroy()
#    exit()


root.geometry("270x75")
root.resizable(False, False)
root.title("EMU Login")
root.iconbitmap('toaster.ico')
root['background'] = '#F0F0F0'
heading = Label(text="Communicating with Mega. Please wait...", font=("Segoe", 10), fg="black", height="2")
heading.place(relx=0.5, rely=0.4, anchor=CENTER)
# SOON:
# register = ttk.Button(root, text="Cancel", command=command)
# register.pack()

root.mainloop()
