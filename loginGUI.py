from tkinter import *
from cryptography.fernet import Fernet
from mega import Mega
from mega import errors
import os


def loginGUI():
    mega = Mega()

    try:
        open("key", "r").read().splitlines()
    except FileNotFoundError:
        open("key", "w+")

    if os.stat("key").st_size == 0:
        key = Fernet.generate_key()
        print(type(key))
        keyWrite = open("key", "wb")
        keyWrite.write(key)
        keyWrite.close()
    else:
        key = open("key", "rb", ).read()

    f = Fernet(bytes(key))

    root = Tk()
    root.geometry("250x260")
    root.resizable(False, False)
    root.title("EMU Login")
    root.iconbitmap('toaster.ico')
    heading = Label(text="Enter login info to Mega.nz", bg="grey", fg="black", width="500", height="3")
    heading.pack()

    email_text = Label(text="E-mail* ", )
    password_text = Label(text="Password* ", )
    email_text.place(x=15, y=70)
    password_text.place(x=15, y=120)
    loginCorrText = Label(text="The login was correct.\n You can now close this and upload.", foreground="lime", justify=LEFT)
    loginerrorText = Label(text="The email or password was incorrect.", foreground="red")
    blanklabel = Label(height=15, width=60)
    blanklabel.place(x=12, y=168)
    loginerrorText.place(x=12, y=168)
    loginCorrText.place(x=12, y=168)

    email = StringVar()
    password = StringVar()

    email_entry = Entry(textvariable=email, width="30")
    password_entry = Entry(textvariable=password, width="30", show="*")

    email_entry.place(x=15, y=100)
    password_entry.place(x=15, y=150)

    register = StringVar()

    def save_info():
        email_info = email.get()
        password_info = password.get()

        def testLogin():
            try:
                mega.login(email=email_info, password=password_info)
            except errors.RequestError:
                loginerrorText.tkraise()
            else:
                loginCorrText.tkraise()
                register.tkraise()
                email_entry.tkraise()
                password_entry.config(state=DISABLED)
                email_entry.config(state=DISABLED)
                try:
                    open("login", "r").read().splitlines()
                except FileNotFoundError:
                    open("login", "w+")
                encodedEmail = email_info.encode()
                encryptedEmail = f.encrypt(encodedEmail)
                encodedPass = password_info.encode()
                encryptedPass = f.encrypt(encodedPass)
                writeLoginB1 = open("login", "wb")
                writeLoginB1.write(encryptedEmail)
                writeLoginB1.write("\n".encode())
                writeLoginB1.write(encryptedPass)
                writeLoginB1.close()

        testLogin()
        email_entry.delete(0, END)
        password_entry.delete(0, END)

    register = Button(root, text="Log in", width="30", height="2", command=save_info, bg="grey")
    register.place(x=15, y=200)

    root.mainloop()
