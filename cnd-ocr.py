from tkinter import *
import pyautogui
from PIL import ImageTk
from pytesseract import image_to_string
import pyperclip

class Application(Frame):
    def __init__(self, master=None):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.box = None

        Frame.__init__(self, master)
        root.title("Hello")


        screen = pyautogui.screenshot()
        conv_screen = ImageTk.PhotoImage(screen)
        screenshot = Label(root, image=conv_screen)
        screenshot.image = conv_screen
        screenshot.pack()
        root.attributes('-fullscreen', True)

        self.boxCanvas = Canvas(root, cursor="cross")
        self.boxCanvas.pack(fill=BOTH, expand=YES)
        root.bind("<Button-1>", self.press)
        root.bind("<B1-Motion>", self.motion)
        root.bind("<ButtonRelease-1>", self.release)

    def press(self, event):
        self.x1 = self.boxCanvas.canvasx(event.x)
        self.y1 = self.boxCanvas.canvasy(event.y)

        self.box = self.boxCanvas.create_rectangle(0, 0, 1, 1, width=3, outline='red', fill='blue')

    def motion(self, event):
        self.x2 = event.x
        self.y2 = event.y
        self.boxCanvas.coords(self.box, self.x1, self.y1, self.x2, self.y2)

    def release(self, event):
        if self.x1 <= self.x2 and self.y1 <= self.y2:
            self.ocr_copy(self.x1, self.y1, self.x2-self.x1, self.y2-self.y1)
        elif self.x1 <= self.x2 and self.y1 >= self.y2:
            self.ocr_copy(self.x2, self.y1, self.x1-self.x2, self.y2-self.y1)
        elif self.x1 >= self.x2 and self.y1 <= self.y2:
            self.ocr_copy(self.x1, self.y2, self.x2-self.x1, self.y1-self.y2)
        elif self.x1 >= self.x2 and self.y1 >= self.y2:
            self.ocr_copy(self.x2, self.y2, self.x1-self.x2, self.y1-self.y2)
        root.destroy()

    def ocr_copy(self, start_x, start_y, end_x, end_y):
        source_screenshot = pyautogui.screenshot(region=(start_x, start_y, end_x, end_y))
        pyperclip.copy(image_to_string(source_screenshot))

root = Tk()
app = Application(master=root)
app.mainloop()

