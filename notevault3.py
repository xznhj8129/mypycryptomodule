#!/usr/bin/python3
#-*- coding: utf-8 -*-
import tkinter as Tkinter
import tkinter.scrolledtext as ScrolledText
import tkinter.filedialog as tkFileDialog
import tkinter.simpledialog as tkSimpleDialog
import tkinter.messagebox as tkMessageBox
from Crypto.Hash import MD5
from Crypto.Hash import SHA256
from tkinter import *
from cryptomodule import *

def encrypt(text, newvector):
    global pw
    global vector
    global pkey
    if newvector: vector = Random.new().read(AES.block_size)
    signature = binascii.b2a_hex((pkey.sign_hash(SHA256.new(bytes(text,'utf-8'))))).decode('utf-8')
    enctext = binascii.b2a_hex(AESencrypt(bytes(text,'utf-8'),bytes(pw,'utf-8'),vector)).decode('utf-8')
    return enctext,signature


def get_password():
    global pw
    entry = tkSimpleDialog.askstring("Input Password", "Enter decryption password",parent=root,show="*")
    if entry == None:
        pw = None
    else:
        pw = MD5.new(bytes(entry,'utf-8')).hexdigest()


def new_command():
    global fileopenopts
    global pw
    global vector
    global title
    global open_file
    file = tkFileDialog.asksaveasfile(parent=root, mode='w', title='Create a file', **fileopenopts)
    if file!=None:
        get_password()
        filename = (file.name.split("/")[len(file.name.split("/"))-1]).split('.')[0]
        enctext,signature = encrypt("",True)
        root.wm_title(title+' - '+file.name)
        file.write(signature + '|' + binascii.b2a_hex(vector).decode('utf-8') + '|' + enctext)
        open_file = file.name
        textPad.delete(1.0,END)
        file.close()


def open_command():
    global fileopenopts
    global pw
    global vector
    global title
    global open_file
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select a file', **fileopenopts)
    if file!=None:
        done = False
        filename = (file.name.split("/")[len(file.name.split("/"))-1]).split('.')[0]
        contents = file.read()
        parts = contents.decode().split('|')
        signature = binascii.a2b_hex(parts[0])
        vector = binascii.a2b_hex(parts[1])
        enctext = binascii.a2b_hex(parts[2])
        while not done:
            get_password()
            if not pw:
                done = True
            else:
                text = AESdecrypt(enctext,bytes(pw,'utf-8'),vector)
                check = pkey.verify_hash(SHA256.new(bytes(text,'utf-8')),signature)
                if check:
                    #tkMessageBox.showinfo(title, "Decryption Successful")
                    textPad.delete(1.0,END)
                    textPad.insert('1.0',text)
                    root.wm_title(title+' - '+file.name)
                    open_file = file.name
                    done = True
                else:
                    tkMessageBox.showinfo(title, "Wrong password!")
        file.close()


def open_command():
    global fileopenopts
    global pw
    global vector
    global title
    global open_file
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select a file', **fileopenopts)
    if file!=None:
        done = False
        filename = (file.name.split("/")[len(file.name.split("/"))-1]).split('.')[0]
        contents = file.read()
        parts = contents.decode().split('|')
        signature = binascii.a2b_hex(parts[0])
        vector = binascii.a2b_hex(parts[1])
        enctext = binascii.a2b_hex(parts[2])
        while not done:
            get_password()
            if not pw:
                done = True
            else:
                text = AESdecrypt(enctext,bytes(pw,'utf-8'),vector)
                check = pkey.verify_hash(SHA256.new(bytes(text,'utf-8')),signature)
                if check:
                    #tkMessageBox.showinfo(title, "Decryption Successful")
                    textPad.delete(1.0,END)
                    textPad.insert('1.0',text)
                    root.wm_title(title+' - '+file.name)
                    open_file = file.name
                    done = True
                else:
                    tkMessageBox.showinfo(title, "Wrong password!")
        file.close()


def save_command():
    global open_file
    if not open_file: save_as_command()
    else: _save_command()


def _save_command():
    global pw
    global vector
    global open_file
    file = open(open_file,mode="w")
    textdata = textPad.get('1.0', END+'-1c')
    enctext,signature = encrypt(textdata,False)
    file.write(signature + '|' + binascii.b2a_hex(vector).decode('utf-8') + '|' + enctext)
    file.close()
    tkMessageBox.showinfo(title, "File saved.")


def save_as_command():
    global fileopenopts
    global pw
    global vector
    global open_file

    file = tkFileDialog.asksaveasfile(mode='w', title='Save as new file', **fileopenopts)
    if file!=None:
        if not pw:
            get_password()
        if not vector:
            vector = Random.new().read(AES.block_size)
        textdata = textPad.get('1.0', END+'-1c')
        enctext, signature = encrypt(textdata,False)
        file.write(signature + '|' + binascii.b2a_hex(vector).decode('utf-8') + '|' + enctext)
        open_file = file.name
        file.close()
        tkMessageBox.showinfo(title, "File saved.")


def exit_command():
    global pw
    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
        pw = Random.new().read(AES.block_size)
        root.destroy()
        exit()


def about_command():
    global version
    tkMessageBox.showinfo("About", "NoteVault "+version+"\nAES-256 Encryption\nPart of MyCryptoSuite\nhttps://github.com/snow-frog/MyCryptoSuite\nGNU GPL v2")

version = "3.1"
pw=None
vector=None
txtfiles=None
open_file=None
#program_key = '-----BEGIN RSA PRIVATE KEY-----\nMIICWwIBAAKBgQCMWL1c0pKHTQ+06qtU1UAVidYSEHCSHUdSk23CRgMGu2yHthpF\nSxeBNeCr32nUo9werGfVUfjzPDviXlIYdTmv5zqyGI/IH3K4JRmPemiP0BdRnN0i\nWzzWzdT01CUX0vtbZIYQPm0JGkZOP/mlIp+eKDEIMkDM5/usSMZWcxZDbQIDAQAB\nAoGAFY5jt2gYXXO2n+ETY7pFV4mOOcQQpkCc/c/rIdXDDTuoVcfgjRgViiEOWxe7\nl497dbKhWCB5DlMIF6LJFTycGXA2wK1amCsjiUvFWZ1H36qI68OTkSpi6WPRq/jV\na3P4YT4/rI37ptWYTvF5VnxMym1+zF7mNq7znHdD916UyAECQQC3mUXDM8PmWHhB\nIrm64uqgWdvmZUOg3jhrtpSYStM/CKwHzH9lCxXKd4E+j/gBt2N+igTORnq+nN/Y\ncZw/1jxtAkEAw7ERFIanJe8oDYD/fd6ILvZRiR1DCJjQKSyskXkCEByrBdNIYFIC\nVfv0YUjrs2orPlkxvFBx3wzR9fDDSn3DAQJAQvDQfc6m85p4Jg+aNmi78UEyKzvq\nv4GmgqdsYGaPxSDNUH6gSGAVTt/psLzfSQjrbty1ydvqrwsVlp49wQzEtQJAO+O/\n33FKTGDB+EgHaSUmtoCp+XWcI1BpPICwm6DWEcpESPcdimTu1BPU+cUQZYtTirRP\ndVuFTgclZsh1bCHLAQJAdpJQ4Ja0gCUBZSPBDpdXEAX5tTwocd4vPkrTXQyYSiRF\nQ9spLnohft7EF23OSNDVJhWd4v+8P+jGjTwbn+/EgQ==\n-----END RSA PRIVATE KEY-----'
pkey = RSA_key()
#pkey.import_key(program_key)
fileopenopts = dict(defaultextension='.nv3', filetypes=[('AES256 Files','*.nv3')])
title=' NoteVault '+version

root = Tkinter.Tk(className=title)
try: root.iconbitmap('padlock1.ico')
except: pass
textPad = ScrolledText.ScrolledText(root, width=100, height=50, fg='green2', bg='black')
textPad.config(insertbackground="green2")
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=new_command)
filemenu.add_command(label="Open file...", command=open_command)
filemenu.add_command(label="Save", command=save_command)
filemenu.add_command(label="Save as...", command=save_as_command)
#filemenu.add_command(label="Open RSA key...", command=open_key)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_command)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about_command)

textPad.pack()
root.mainloop()
