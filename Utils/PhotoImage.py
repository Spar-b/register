from PIL import Image, ImageTk

class PhotoImage:
    def __init__(self, filename):
        self.image = Image.open(filename)
        self.photo = ImageTk.PhotoImage(self.image)