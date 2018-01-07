import sys
import os
import subprocess, os, errno, shutil
import tkinter as tk
from tkinter import ttk
import os.path
import OpenImageIO as oiio
import OpenEXR
import glob
import shlex, subprocess
from subprocess import check_output
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import showerror
import tkinter.messagebox
from _thread import start_new_thread

global ORIGINAL_PATHANDFILE
global ORIGINAL_PATH #was path
global ORIGINAL_FILENAME
global FILECOUNT
global TEXSIZE
global TEXPAT
global TEXEXT
global TEXNAME
global NEW_ORIGINAL_PATH
global NEW_TEXSIZE
global USER_INPUT
global USER_INPUT_COUNT

FILECOUNT = 0
ORIGINAL_PATHANDFILE = 'null'
#
types = ('*.exr', '*.tif')
files_grabbed = []
for files in types:
    files_grabbed.extend(glob.glob(files))
"""
subprocess.call('oiiotool.exe test2.exr --resize 200x200 -o out22.exr', shell=True)
print(str(files_grabbed))
"""




class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        
    def quit(self):
        global root
        root.quit()

    def CreateOriginalDir(self):
        cwd = os.getcwd()
        newpath = os.path.join(original__path,'ORIGINAL_TEXTURES')
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        #ORIGINAL_PATH = cwd
        global new_backup_path
        new_backup_path = newpath



    def ProcessTextureList(self):
        

        if user_input:
            global input_fileList
            input_fileList = root.tk.splitlist(user_input)

            for texfile in input_fileList:
                global original__path_and_filename
                original__path_and_filename = texfile
                global original__filename
                global original__path
                #print(str(ORIGINAL_PATHANDFILE)) #prints as C:/Users/thele/Documents/GitHub/supersizeme/test2b.exr
                original__path, original__filename = os.path.split(texfile)

                self.CreateOriginalDir()
                self.DownsizeTexture(original__path, original__filename)

                #print(str(ORIGINAL_PATH))
                global extension
                extension = os.path.splitext(original__filename)[1]
                global filenameWithoutExtension
                filenameWithoutExtension, junk = original__filename.split(extension)

                #self.DownsizeTexture()

        '''
        types = ('*.exr', '*.tif')
        files_grabbed = []
        for files in types:
            files_grabbed.extend(glob.glob(files))
        '''

    def DownsizeTexture(self, arg1, arg2):

        #backup the file
        global fullpathname
        fullpathname = arg1 + "\\" + arg2
        global backupfullname
        backupfullname = new_backup_path + "\\" +  arg2
        
        #print(fullpathname)
        #print(backupfullname)
        
        shutil.copy(fullpathname, backupfullname)

        #resize the backup

        print(original__filename)
 
        global resolution
        argFileIn = backupfullname
        print(argFileIn)
        argFileOut = fullpathname
        resolution = 256
        argRes = str(resolution) + "x" + str(resolution)
        print(argRes)
        subprocess.call('oiiotool.exe'+' '+ argFileIn + ' --resize ' + argRes + ' -o ' + argFileOut, shell=True)
        
    def create_widgets(self):
        
        title = tk.StringVar()
        title.set('superresizeme')
        w = tk.Label(self, textvariable=title, font=("Helvetica", 16))
        w.pack()

        #run
        superresizemeBox = tk.Button(self, fg="orange")
        superresizemeBox["text"] = "superresizeme!"
        superresizemeBox["command"] = self.ProcessTextureList
        superresizemeBox.pack(side="top")



        global var
        var = tk.StringVar()
        var.set("default")
        y = 200 # for separater

        global TEX256
        global TEX512
        global TEX1024
        global TEX2048
        global REPLACEORIGINAL
        global CREATEFILES
        REPLACEORIGINAL = tk.BooleanVar()
        REPLACEORIGINAL.set(False)
        CREATEFILES = tk.BooleanVar()
        CREATEFILES.set(True)


        TEX256 = tk.BooleanVar()
        TEX256.set(True)
        TEX512 = tk.BooleanVar()
        TEX512.set(False)
        TEX1024 = tk.BooleanVar()
        TEX1024.set(False)
        TEX2048 = tk.BooleanVar()
        TEX2048.set(False)

        global label
        label = tk.Label(self, text=str(FILECOUNT) + " files selected")
        label.pack()

        #select files box
        selectFilesBox = tk.Button(self, fg="green")
        selectFilesBox["text"] = "Select files"
        selectFilesBox["command"] = self.load_files
        selectFilesBox.pack(side="top")

        #sep
        sep = ttk.Separator(self,orient=tk.HORIZONTAL)
        sep.pack(side="top", fill="y",ipady=5)

        # checkboxes
        chk = tk.Checkbutton(self, name="checkbox_Test",activebackground='yellow',activeforeground='yellow',variable=CREATEFILES,cursor='arrow',indicatoron=0,selectcolor='green')
        chk["command"] = print("-")#self.checkbxTestDef
        chk["text"] = "Resize files"
        chk.pack(side="top")

        # texture size selection
        chk256 = tk.Checkbutton(self, name="checkbox_Tex256",activebackground='yellow',activeforeground='yellow',variable=TEX256,cursor='arrow',indicatoron=0,selectcolor='cyan')
        chk256["command"] = self.SetTextureSize(256)
        chk256["text"] = "256"
        chk256.pack(side="top")
        chk512 = tk.Checkbutton(self, name="checkbox_Tex512",activebackground='yellow',activeforeground='yellow',variable=TEX512,cursor='arrow',indicatoron=0,selectcolor='cyan')
        chk512["command"] = self.SetTextureSize(512)
        chk512["text"] = "512"
        chk512.pack(side="top")
        chk1024 = tk.Checkbutton(self, name="checkbox_Tex1024",activebackground='yellow',activeforeground='yellow',variable=TEX1024,cursor='arrow',indicatoron=0,selectcolor='cyan')
        chk1024["command"] = self.SetTextureSize(1024)
        chk1024["text"] = "1024"
        chk1024.pack(side="top")
        chk2048 = tk.Checkbutton(self, name="checkbox_Tex2048",activebackground='yellow',activeforeground='yellow',variable=TEX2048,cursor='arrow',indicatoron=0,selectcolor='cyan')
        chk2048["command"] = self.SetTextureSize(2048)
        chk2048["text"] = "2048"
        chk2048.pack(side="top")

        sep = ttk.Separator(self,orient=tk.HORIZONTAL)
        sep.pack(side="top", fill="y",ipady=5)

        # danger zone
        chkRepealandreplace = tk.Checkbutton(self, name="checkbox_Replace",activebackground='yellow',activeforeground='yellow',variable=REPLACEORIGINAL,cursor='arrow',indicatoron=0,selectcolor='red')
        chkRepealandreplace["command"] = print("-")#self.checkbxTestDef
        chkRepealandreplace["text"] = "Replace original"
        chkRepealandreplace.pack(side="top")

        sep = ttk.Separator(self,orient=tk.HORIZONTAL)
        sep.pack(side="right", fill="y",ipady=15)

        #debugbutton
        debugbutton = tk.Button(self, fg="green")
        debugbutton["text"] = "createdir"
        debugbutton["command"] = self.CreateOriginalDir
        debugbutton.pack(side="top")

        sep = ttk.Separator(self,orient=tk.HORIZONTAL)
        sep.pack(side="right", fill="y",ipady=15)

        quit = tk.Button(self, fg="red")
        quit["text"] = "Quit"
        quit["command"] = self.quit
        quit.pack(side="bottom")

    def load_files(self):
        cwd = os.getcwd()
        global user_input
        user_input = askopenfilenames(initialdir = cwd, title = "Select file",filetypes = (("exr","*.exr"),("all","*.*")))
        #file_count = str(len(user_input))
        #self.label.configure(text= str(len(user_input))) # error no label found

        self.ProcessTextureList()
        
        #root.mainloop()
        #label.update_idletasks() # error no label found

    def SetTextureSize(self, arg):
        print('-')
        #global resolution
        #resolution = arg
        #print(resolution)

# Create root window object
root = tk.Tk()
root.title("superresizeme")
root.tk.call('wm', 'iconbitmap', root._w, '-default', 'icon.ico')
root.minsize(200,325)
root.maxsize(200, 400)

app = Application(master=root)
app.mainloop()