from PIL import Image,ImageTk
import tkinter as tk

screen_height = 750
screen_width = 420


def clear_widgets(root):
    # This function is used everytime a new page is launched to clear everything from the previous page.

    for i in root.winfo_children():
        i.destroy()


def resizing_images(root,
           background_image_path,
           second_image_path,
           screen_width,
           screen_height,
           resized_width,
           resized_height,
           x_pos,
           y_pos
           ):
    """
    The Function we put together in class to resize images on top of other images to use brackground images in combination with other images.
    """
    global pic, f1

    f1 = tk.Frame(root)

    img1 = Image.open(background_image_path)
    img1 = img1.resize((screen_width, screen_height), Image.LANCZOS)

    img2 = Image.open(second_image_path)
    img2 = img2.resize((resized_width, resized_height), Image.LANCZOS)

    img1.paste(img2, (x_pos, y_pos))

    pic = ImageTk.PhotoImage(img1)
    Lab = tk.Label(f1, image=pic)
    Lab.pack()
    f1.pack()