import os
import threading

import argparse
from cryptography.fernet import Fernet
from sys import exit
from packaging import version
from tkinter import messagebox
import sys
import gui
import loginGUI
import requests
import webbrowser
from tkinter import Tk

import pyperclip
import win10toast
from mega import Mega
from mega import errors

if getattr(sys, 'frozen', False):
    VERSION = open("VERSION", "r").read().splitlines()
    versionFile = requests.get(
        r"https://raw.githubusercontent.com/CUPZYY/EasyMegaUpload/main/VERSION").text.splitlines()
    var = version.parse(VERSION[0]) < version.parse(versionFile[0])
    if var:
        root = Tk()
        root.withdraw()
        root.protocol("WM_DELETE_WINDOW", exit)
        versionFile = requests.get(
            r"https://raw.githubusercontent.com/CUPZYY/EasyMegaUpload/main/VERSION").text.splitlines()
        updatePrompt = messagebox.askquestion("Update Available!",
                                              f"There is a newer version of the program available (v{versionFile[0]}). Would you like to download it now?")
        if updatePrompt[0] == "y":
            webbrowser.open(versionFile[1])
            exit()
        else:
            exit()

mega = Mega()
toaster = win10toast.ToastNotifier()
gui = gui.guiClass()
uploading = False
appdata = os.getenv('APPDATA')
appdataFolder = f"{appdata}\\EasyMegaUpload"

# if len(sys.argv) > 1:
#   filepath = sys.argv[1]
#   print(filepath)
# else:
#    filepath = sys.argv[0]

if not os.path.exists(appdataFolder):
    os.mkdir(appdataFolder)

parser = argparse.ArgumentParser(description="Uploads files to mega, easily")
parser.add_argument("-p", "--path", type=str, metavar="", help="The filepath to the file you want to upload",
                    required=True)
args = parser.parse_args()

filepath = args.path

try:
    loginread = open(fr"{appdataFolder}\login", "r").read().splitlines()
except FileNotFoundError:
    loginGUI.loginGUI()
    exit()

if os.stat(fr"{appdataFolder}\login").st_size == 0:
    loginGUI.loginGUI()
    exit()


def init():
    try:
        loginread[1]
    except IndexError:
        loginGUI.loginGUI()
        exit()
    try:
        open(fr"{appdataFolder}\key", "r").read().splitlines()
    except FileNotFoundError:
        loginGUI.loginGUI()
        exit()
    if os.stat(fr"{appdataFolder}\key").st_size == 0:
        loginGUI.loginGUI()
        exit()
    else:
        key = open(fr"{appdataFolder}\key", "rb", ).read()
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


def upload():
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
        return
    folderName = "EasyUpload"
    findfolder = m.find(folderName)
    if findfolder is None:
        m.create_folder(folderName)
    try:
        file = m.upload(filepath, findfolder[0])
        fileurl = m.get_upload_link(file)
    except:
        unsuccessToaster()
        return
    pyperclip.copy(fileurl)
    successToaster()
    return


uplfoadThread = threading.Thread(target=gui.gui)
uplfoadThread.setDaemon(True)
uplfoadThread.start()
upload()
exit()
