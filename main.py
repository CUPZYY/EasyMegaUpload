import os
from cryptography.fernet import Fernet
from sys import exit
import sys
import multiprocessing
import gui
import loginGUI

import pyperclip
import win10toast
from mega import Mega
from mega import errors

mega = Mega()
toaster = win10toast.ToastNotifier()
filepath = sys.argv[1]
uploading = False

try:
    loginread = open("login", "r").read().splitlines()
except FileNotFoundError:
    loginGUI.loginGUI()
    exit()

if os.stat("login").st_size == 0:
    loginGUI.loginGUI()
    exit()


def init():
    try:
        sys.argv[1]
    except IndexError:
        raise IndexError("No file to upload")
    try:
        loginread[1]
    except IndexError:
        loginGUI.loginGUI()
        exit()
    try:
        open("key", "r").read().splitlines()
    except FileNotFoundError:
        loginGUI.loginGUI()
        exit()
    if os.stat("key").st_size == 0:
        loginGUI.loginGUI()
        exit()
    else:
        key = open("key", "rb", ).read()
    global f
    f = Fernet(bytes(key))


init()


def passToaster():
    toaster.show_toast("EasyMegaUpload",
                       f"The email/password was incorrect.\nPlease try again",
                       icon_path="toaster.ico",
                       duration=0,
                       threaded=True)


def passToaster():
    toaster.show_toast("EasyMegaUpload",
                       f"The email/password was incorrect.\nPlease try again",
                       icon_path="toaster.ico",
                       duration=0,
                       threaded=True)


def successToaster():
    toaster.show_toast(title="EasyMegaUpload",
                       msg=f"Successfully uploaded {os.path.basename(filepath)}\nThe link was copied to your clipboard",
                       icon_path="toaster.ico",
                       duration=0,
                       threaded=True)


def unsuccessToaster():
    toaster.show_toast("EasyMegaUpload",
                       f"Unsuccessfully uploaded {os.path.basename(filepath)}",
                       icon_path="toaster.ico",
                       duration=0,
                       threaded=True)


if __name__ == "__main__":
    guiProcess = multiprocessing.Process(target=gui.gui)
    guiProcess.start()


def uploading(guiProcessPar):
    try:
        emailencoded = loginread[0].encode()
        passencoded = loginread[1].encode()
        emailDecrypted = f.decrypt(emailencoded)
        passDecrypted = f.decrypt(passencoded)
        emaildecoded = emailDecrypted.decode()
        passdecoded = passDecrypted.decode()
        m = mega.login(email=str(emaildecoded), password=str(passdecoded))
    except errors.RequestError:
        passToaster()
        guiProcessPar.terminate()
        exit()
    folderName = "EasyUpload"
    findfolder = m.find(folderName)
    if findfolder is None:
        m.create_folder(folderName)
    try:
        file = m.upload(filepath, findfolder[0])
        fileurl = m.get_upload_link(file)
    except:
        unsuccessToaster()
        guiProcessPar.terminate()
        exit()
    pyperclip.copy(fileurl)
    successToaster()
    guiProcessPar.terminate()


if __name__ == "__main__":
    uploadingProcess = multiprocessing.Process(target=uploading(guiProcessPar=guiProcess))
    uploadingProcess.start()
