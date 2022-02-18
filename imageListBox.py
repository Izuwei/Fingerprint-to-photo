from tkinter import *
from PIL import ImageTk, Image
import glob


class ImageListBox:
    def __init__(self, root, folder, guiRenderPhoto):
        self.files = glob.glob(folder + "/*.png") + glob.glob(folder + "/*.jpg") + glob.glob(folder + "/*.bmp")
        self.filepath = ""

        self.l = Listbox(root, width=30, height=4)
        self.l.pack()
        self.l.bind("<<ListboxSelect>>", self.imageShow)

        self.c = Label(root)
        self.c.pack()

        self.guiRenderPhoto = guiRenderPhoto

        for f in self.files:
            self.l.insert(END, f)

        if self.files:
            self.filepath = self.files[0]
            self.initalImageShow(self.filepath)

    def initalImageShow(self, path):
        img = ImageTk.PhotoImage(Image.open(path).resize((40, 40)))
        self.c.image = img
        self.c.configure(image=img)
        self.c.pack()

    def imageShow(self, event):
        path = self.getFilename()
        if path == "":
            return
        img = ImageTk.PhotoImage(Image.open(path).resize((40, 40)))
        self.c.image = img
        self.c.configure(image=img)
        self.c.pack()
        self.filepath = path
        self.guiRenderPhoto()

    def getFilename(self):
        n = self.l.curselection()
        if n == ():  # if selected nothing, curselection() returns empty tuple
            return ""
        return self.files[n[0]]
