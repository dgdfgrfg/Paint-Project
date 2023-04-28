import os
import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageTk
from PIL import ImageGrab

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Paint")

        self.pen_color = "black"
        self.brush_size = 5
        self.tool = "brush"
        self.fill = False
        self.points = []

        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save As", command=self.save)
        file_menu.add_command(label="Undo", command=self.undo)

        brush_menu = tk.Menu(menu)
        menu.add_cascade(label="Brush", menu=brush_menu)
        brush_menu.add_command(label="Choose Color", command=self.choose_color)
        brush_menu.add_command(label="Eraser", command=self.use_eraser)
        brush_menu.add_separator()
        brush_menu.add_command(label="Small", command=lambda: self.set_brush_size(2))
        brush_menu.add_command(label="Medium", command=lambda: self.set_brush_size(5))
        brush_menu.add_command(label="Large", command=lambda: self.set_brush_size(10))

        shape_menu = tk.Menu(menu)
        menu.add_cascade(label="Shape", menu=shape_menu)
        shape_menu.add_command(label="Rectangle", command=lambda: self.set_tool("rectangle"))
        shape_menu.add_command(label="Oval", command=lambda: self.set_tool("oval"))
        shape_menu.add_command(label="Line", command=lambda: self.set_tool("line"))
        shape_menu.add_separator()
        shape_menu.add_checkbutton(label="Fill", variable=tk.BooleanVar(value=self.fill), command=self.toggle_fill)

        self.status_bar = tk.Label(self.root, text="Tool: Brush | Brush Size: " + str(self.brush_size) + " | Color: " + self.pen_color, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.palette_frame = tk.Frame(self.root, height=40)
        self.palette_frame.pack(side=tk.BOTTOM, fill=tk.X)

        colors = ["black", "gray", "red", "orange", "yellow", "green", "blue", "purple", "pink", "white"]
        for color in colors:
            button = tk.Button(self.palette_frame, bg=color, width=3, height=2, relief=tk.RAISED,
                               command=lambda col=color: self.set_pen_color(col))
            button.pack(side=tk.LEFT, padx=1, pady=1)
        self.drawn_items = []

    def on_press(self, event):
        self.points = [(event.x, event.y)]

    def paint(self, event):
        if self.tool == "brush":
            item = self.canvas.create_oval(event.x - self.brush_size, event.y - self.brush_size,
                                           event.x + self.brush_size, event.y + self.brush_size,
                                           fill=self.pen_color, outline=self.pen_color)
            self.drawn_items.append(item)
        elif self.tool in ["rectangle", "oval", "line"]:
            self.points.append((event.x, event.y))
            self.reset(event)

    def reset(self, event):
        if self.tool in ["rectangle", "oval", "line"]:
            x1, y1 = self.points[0]
            x2, y2 = event.x, event.y
            self.canvas.delete("temp")
            if self.tool == "rectangle":
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.pen_color, width=self.brush_size, fill=self.pen_color if self.fill else "", tags="temp")
            elif self.tool == "oval":
                self.canvas.create_oval(x1, y1, x2, y2, outline=self.pen_color, width=self.brush_size, fill=self.pen_color if self.fill else "", tags="temp")
            elif self.tool == "line":
                self.canvas.create_line(x1, y1, x2, y2, fill=self.pen_color, width=self.brush_size, tags="temp")

        if event.type == "4":  # ButtonRelease event
            self.canvas.delete("temp")
            if self.tool in ["rectangle", "oval", "line"]:
                x1, y1 = self.points[0]
                x2, y2 = event.x, event.y
                if self.tool == "rectangle":
                    item = self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.pen_color, width=self.brush_size, fill=self.pen_color if self.fill else "")
                elif self.tool == "oval":
                    item = self.canvas.create_oval(x1, y1, x2, y2, outline=self.pen_color, width=self.brush_size, fill=self.pen_color if self.fill else "")
                elif self.tool == "line":
                    item = self.canvas.create_line(x1, y1, x2, y2, fill=self.pen_color, width=self.brush_size)
                self.drawn_items.append(item)
                self.points = []

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.status_bar.config(text="Tool: " + self.tool.capitalize() + " | Brush Size: " + str(self.brush_size) + " | Color: " + self.pen_color)

    def use_eraser(self):
        self.pen_color = "white"

    def set_brush_size(self, size):
        self.brush_size = size
        self.status_bar.config(text="Tool: " + self.tool.capitalize() + " | Brush Size: " + str(self.brush_size) + " | Color: " + self.pen_color)

    def set_pen_color(self, col):
        self.pen_color = col
        self.status_bar.config(text="Tool: " + self.tool.capitalize() + " | Brush Size: " + str(self.brush_size) + " | Color: " + self.pen_color)

    def set_tool(self, tool):
        self.tool = tool
        self.status_bar.config(text="Tool: " + self.tool.capitalize() + " | Brush Size: " + str(self.brush_size) + " | Color: " + self.pen_color)

    def toggle_fill(self):
        self.fill = not self.fill

    def save(self):
        file = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("Portable Network Graphics", "*.png"),
                                                       ("JPEG", "*.jpg;*.jpeg"),
                                                       ("Bitmap Image", "*.bmp"),
                                                       ("All files", "*.*")])
        if file:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(file)

    def undo(self):
        if self.drawn_items:
            self.canvas.delete(self.drawn_items[-1])
            self.drawn_items.pop()

if __name__ == "__main__":
    root = tk.Tk()
    PaintApp(root)
    root.mainloop()

