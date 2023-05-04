import os
import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog
from PIL import Image, ImageTk
from PIL import ImageGrab

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Paint")
        self.drawn_items = []
        self.current_shape = None

        self.pen_color = "black"
        self.brush_size = 5
        self.tool = "brush"
        self.fill = False
        self.points = []

        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

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
        brush_menu.add_command(label="Custom", command=self.choose_brush_size)

        shape_menu = tk.Menu(menu)
        menu.add_cascade(label="Shape", menu=shape_menu)
        shape_menu.add_command(label="Brush", command=lambda: self.set_tool("brush"))
        shape_menu.add_command(label="Hexagon", command=lambda: self.set_tool("hexagon"))
        shape_menu.add_command(label="Octagon", command=lambda: self.set_tool("octagon"))
        shape_menu.add_command(label="Star", command=lambda: self.set_tool("star"))
        shape_menu.add_command(label="Arrow", command=lambda: self.set_tool("arrow"))
        shape_menu.add_command(label="Square", command=lambda: self.set_tool("square"))
        shape_menu.add_command(label="Circle", command=lambda: self.set_tool("circle"))
        shape_menu.add_command(label="Rectangle", command=lambda: self.set_tool("rectangle"))
        shape_menu.add_command(label="Oval", command=lambda: self.set_tool("oval"))
        shape_menu.add_command(label="Line", command=lambda: self.set_tool("line"))
        shape_menu.add_command(label="Triangle", command=lambda: self.set_tool("triangle"))
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

    def set_pen_color(self, color):
        self.pen_color = color
        self.status_bar.config(text=f"Tool: {self.tool} | Brush Size: {self.brush_size} | Color: {self.pen_color}")

    def set_tool(self, tool):
        self.tool = tool
        self.status_bar.config(text=f"Tool: {self.tool} | Brush Size: {self.brush_size} | Color: {self.pen_color}")

    def choose_color(self):
        color = colorchooser.askcolor(color=self.pen_color)[1]
        if color:
            self.set_pen_color(color)

    def set_brush_size(self, size):
        self.brush_size = size
        self.status_bar.config(text=f"Tool: {self.tool} | Brush Size: {self.brush_size} | Color: {self.pen_color}")

    def choose_brush_size(self):
        size = simpledialog.askinteger("Brush Size", "Enter brush size:", minvalue=1, maxvalue=100, initialvalue=self.brush_size)
        if size:
            self.set_brush_size(size)

    def use_eraser(self):
        self.set_pen_color("white")

    def on_press(self, event):
        self.points = [(event.x, event.y)]
        if self.tool != "brush":
            self.current_shape = None

    def on_release(self, event):
        if self.tool != "brush" and self.current_shape:
            self.drawn_items.append(self.current_shape)
            self.current_shape = None
        self.points = []

    def paint(self, event):
        if self.tool == "brush":
            self.canvas.create_line(self.points[-1], (event.x, event.y), width=self.brush_size, fill=self.pen_color, capstyle=tk.ROUND, smooth=True)
            self.points.append((event.x, event.y))
        else:
            self.points.append((event.x, event.y))
            if len(self.points) >= 2:
                self.resize_shape()
                self.points.pop()

    def resize_shape(self):
        start_x, start_y = self.points[0]
        end_x, end_y = self.points[1]
        coords = (start_x, start_y, end_x, end_y)

        if self.fill:
            fill = self.pen_color
        else:
            fill = ""

        if self.current_shape:
            self.canvas.delete(self.current_shape)

        if self.tool == "line":
            shape = self.canvas.create_line(coords, width=self.brush_size, fill=self.pen_color, capstyle=tk.ROUND)
        elif self.tool == "square":
            shape = self.canvas.create_rectangle(coords, width=self.brush_size, outline=self.pen_color, fill=fill)
        elif self.tool == "octagon":
            shape = self.create_octagon(coords, width=self.brush_size, outline=self.pen_color, fill=fill)

        elif self.tool == "circle":
            shape = self.canvas.create_oval(coords, width=self.brush_size, outline=self.pen_color, fill=fill)
        elif self.tool == "rectangle":
            shape = self.canvas.create_rectangle(coords, width=self.brush_size, outline=self.pen_color, fill=fill)
        elif self.tool == "oval":
            shape = self.canvas.create_oval(coords, width=self.brush_size, outline=self.pen_color, fill=fill)
        elif self.tool == "triangle":
            x1, y1, x2, y2 = coords
            x3, y3 = x1, y2
            shape = self.canvas.create_polygon((x1, y1, x2, y2, x3, y3), width=self.brush_size, outline=self.pen_color, fill=fill)
        elif self.tool == "hexagon":
            shape = self.create_hexagon(coords, width=self.brush_size, outline=self.pen_color, fill=fill)
        elif self.tool == "star":
            shape = self.create_star(coords, width=self.brush_size, outline=self.pen_color, fill=fill)
        elif self.tool == "arrow":
            shape = self.create_arrow(coords, width=self.brush_size, outline=self.pen_color, fill=fill)

        self.current_shape = shape

    def create_hexagon(self, coords, **kwargs):
        x1, y1, x2, y2 = coords
        width = x2 - x1
        height = y2 - y1
        dx = width / 4
        dy = height / 2

        hexagon_points = (
            x1 + dx, y1,
            x1 + 3 * dx, y1,
            x2, y1 + dy,
            x1 + 3 * dx, y2,
            x1 + dx, y2,
            x1, y1 + dy
        )
        return self.canvas.create_polygon(hexagon_points, **kwargs)

    def create_star(self, coords, **kwargs):
        x1, y1, x2, y2 = coords
        x_mid = (x1 + x2) / 2
        y_mid = (y1 + y2) / 2

        star_points = (x_mid, y1, x2, y2, x1, y2)
        return self.canvas.create_polygon(star_points, **kwargs)

    def create_arrow(self, coords, **kwargs):
        x1, y1, x2, y2 = coords
        width = x2 - x1
        height = y2 - y1
        dx = width / 3
        dy = height / 6

        arrow_points = (
            x1, y1 + 2 * dy,
            x1 + 2 * dx, y1 + 2 * dy,
            x1 + 2 * dx, y1,
            x2, y1 + height / 2,
            x1 + 2 * dx, y2,
            x1 + 2 * dx, y1 + 4 * dy,
            x1, y1 + 4 * dy
        )
        return self.canvas.create_polygon(arrow_points, **kwargs)
    
    def create_octagon(self, coords, **kwargs):
        x1, y1, x2, y2 = coords
        width = x2 - x1
        height = y2 - y1
        dx = width / 4
        dy = height / 4

        octagon_points = (
            x1 + dx, y1,
            x1 + 3 * dx, y1,
            x2, y1 + dy,
            x2, y1 + 3 * dy,
            x1 + 3 * dx, y2,
            x1 + dx, y2,
            x1, y1 + 3 * dy,
            x1, y1 + dy
        )
        return self.canvas.create_polygon(octagon_points, **kwargs)

    def reset(self, event):
        self.points = []

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
            item = self.drawn_items.pop()
            self.canvas.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    PaintApp(root)
    root.mainloop()

