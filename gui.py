from tkinter import *
import tkinter.ttk
from PIL import ImageTk, Image
from tkinter import filedialog

from imageListBox import ImageListBox
from main import get_fingerprint_photo

# Window config
root = Tk()
root.title("Synthetic fingerprint to photo")
root.resizable(False, False)
icon = PhotoImage(file="./assets/fingerprint-icon.png")
root.iconphoto(False, icon)

# Methods
photo_img = None


def importImage():
    filetypes = (("Image files", "*.png *.jpg *.bmp"),)
    fingerprintFilename = filedialog.askopenfilename(
        title="Select a fingerprint", initialdir="/", filetypes=filetypes
    )
    if fingerprintFilename != "":
        fingerprint = Image.open(fingerprintFilename)
        fingerprint.thumbnail((600, 600))
        fingerprint = ImageTk.PhotoImage(fingerprint)
        fingerprintImage.img = fingerprint  # keeps garbage collected away
        fingerprintImage["image"] = fingerprint
        fingerprintListBox.filepath = fingerprintFilename
        renderPhoto(fingerprintFilename)
    print(fingerprintFilename)


def saveImage():
    if photo_img:
        file = filedialog.asksaveasfile(
            mode="wb",
            filetypes=[("png", "*.png")],
            defaultextension=".png",
            initialfile="fingerprint",
        )
        if file:
            photo_img.save(file)


def renderPhoto(fingerprintFilename=""):
    if not fingerprintFilename:
        fingerprintFilename = fingerprintListBox.filepath

    fingerprint = Image.open(fingerprintFilename)
    fingerprint.thumbnail((600, 600))
    fingerprint = ImageTk.PhotoImage(fingerprint)
    fingerprintImage.img = fingerprint
    fingerprintImage["image"] = fingerprint

    skinFilename = skinListBox.filepath
    backgroundFilename = backgroundListBox.filepath
    damageFilename = damageListBox.filepath
    if fingerprintFilename and skinFilename and backgroundFilename and damageFilename:
        global photo_img
        photo_img = get_fingerprint_photo(
            fingerprintFilename, skinFilename, backgroundFilename, damageFilename
        )
        photo = photo_img.copy()
        photo.thumbnail((600, 600))
        photo = ImageTk.PhotoImage(photo)
        photoImage.img = photo
        photoImage["image"] = photo


### Panel section ###


tkinter.ttk.Separator(root, orient=VERTICAL).grid(
    column=3, row=0, rowspan=25, sticky="ns"
)
panelLabel = Label(root, text="Preferences", font=("Helvetica", 16, "bold"))
panelLabel.grid(row=0, column=4, pady=(10, 15))

# Fingerprint frame
fingerprintFrame = LabelFrame(
    root, text="Fingerprint", font=("Helvetica", 11), padx=5, pady=5
)
fingerprintFrame.grid(row=1, column=4, rowspan=5, padx=10, pady=0)

fingerprintListBox = ImageListBox(
    fingerprintFrame, "./assets/fingerprints", renderPhoto
)

# Skin frame
skinFrame = LabelFrame(root, text="Skin", font=("Helvetica", 11), padx=5, pady=5)
skinFrame.grid(row=6, column=4, rowspan=5, padx=10, pady=0)

skinListBox = ImageListBox(skinFrame, "./assets/skins", renderPhoto)

# Damage frame
damageFrame = LabelFrame(root, text="Damage", font=("Helvetica", 11), padx=5, pady=5)
damageFrame.grid(row=11, column=4, rowspan=5, padx=10, pady=0)

damageListBox = ImageListBox(damageFrame, "./assets/damage", renderPhoto)

# Background frame
backgroundFrame = LabelFrame(
    root, text="Background", font=("Helvetica", 11), padx=5, pady=5
)
backgroundFrame.grid(row=16, column=4, rowspan=5, padx=10, pady=0)

backgroundListBox = ImageListBox(backgroundFrame, "./assets/backgrounds", renderPhoto)


### Fingerprint section ###


fingerprintLabel = Label(root, text="Fingerprint", font=("Helvetica", 16, "bold"))
fingerprint = Image.open(fingerprintListBox.filepath)
fingerprint.thumbnail((600, 600))
fingerprint = ImageTk.PhotoImage(fingerprint)
fingerprintImage = Label(root, image=fingerprint)

fingerprintLabel.grid(row=0, column=0, pady=(10, 15))
fingerprintImage.grid(row=1, column=0, padx=(15, 15), rowspan=20)

importButton = Button(
    root,
    text="Import",
    font=("Helvetica", 11, "bold"),
    padx=40,
    border=0,
    bg="#03a9f4",
    fg="white",
    command=importImage,
)
importButton.grid(row=21, column=0, pady=(15, 15))


### Photo section ###


photoLabel = Label(root, text="Photo", font=("Helvetica", 16, "bold"))
photoImage = Label(root)

photoLabel.grid(row=0, column=1, pady=(10, 15))
photoImage.grid(row=1, column=1, padx=(15, 15), rowspan=20)

saveButton = Button(
    root,
    text="Save",
    font=("Helvetica", 11, "bold"),
    padx=40,
    border=0,
    bg="#43a047",
    fg="white",
    command=saveImage,
)
saveButton.grid(row=21, column=1, pady=(15, 15))


### Main loop ###
renderPhoto()
root.mainloop()
