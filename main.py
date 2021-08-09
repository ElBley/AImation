from tkinter import *
from tkinter import ttk, colorchooser


class main:
    def __init__(self, master):
        self.master = master
        self.color_fg = 'black'
        self.color_fg2 = 'white'
        self.color_bg = 'white'

        self.tools = ['brush', 'line', 'rectangle', 'oval']

        self.selectedTool = self.tools[0]

        self.lineStartX = None
        self.lineStartY = None

        self.stack = []
        self.redoStack = []
        self.Line_objects = []
        self.brushObjets = []

        self.penwidth = 5
        self.drawWidgets()
        self.c.bind('<Button-1>', self.startDraw)
        self.c.bind('<B1-Motion>', self.drawMotion)  # drawing the line
        self.c.bind('<ButtonRelease-1>', self.endDraw)

    def changeTool(self, t: int):
        self.selectedTool = self.tools[t]

    def startDraw(self, e):
        if self.selectedTool == self.tools[0]:
            self.startBrushDraw(e)
        elif self.selectedTool == self.tools[1]:
            self.startLineDraw(e)
        elif self.selectedTool == self.tools[2]:
            self.startRectangleDraw(e)
        elif self.selectedTool == self.tools[3]:
            self.startOvalDraw(e)

    def drawMotion(self, e):
        if self.selectedTool == self.tools[0]:
            self.drawBrushMotion(e)
        elif self.selectedTool == self.tools[1]:
            self.drawLineMotion(e)
        elif self.selectedTool == self.tools[2]:
            self.drawRectangleMotion(e)
        elif self.selectedTool == self.tools[3]:
            self.drawOvalMotion(e)

    def endDraw(self, e):
        if self.selectedTool == self.tools[0]:
            self.endBrushDraw(e)
        elif self.selectedTool == self.tools[1]:
            self.endLineDraw(e)
        elif self.selectedTool == self.tools[2]:
            self.endRectangleDraw(e)
        elif self.selectedTool == self.tools[3]:
            self.endOvalDraw(e)

    def startLineDraw(self, e):
        self.lineStartX = e.x
        self.lineStartY = e.y

    def startBrushDraw(self, e):
        line = self.c.create_line(e.x, e.y, e.x, e.y, width=self.penwidth, fill=self.color_fg, smooth=1, capstyle=ROUND)
        self.brushObjets.append(line)
        self.lineStartX = e.x
        self.lineStartY = e.y

    def startRectangleDraw(self,e):
        self.lineStartX = e.x
        self.lineStartY = e.y

    def startOvalDraw(self,e):
        self.lineStartX = e.x
        self.lineStartY = e.y

    def drawLineMotion(self, e):

        self.c.delete('temp_objects')
        self.c.create_line(self.lineStartX, self.lineStartY, e.x, e.y, fill=self.color_fg, width=self.penwidth,
                           smooth=1, tags='temp_objects')

    def drawBrushMotion(self, e):
        line = self.c.create_line(self.lineStartX, self.lineStartY, e.x, e.y, width=self.penwidth, fill=self.color_fg,
                                  smooth=1, capstyle=ROUND)
        self.brushObjets.append(line)
        self.lineStartX = e.x
        self.lineStartY = e.y

    def drawRectangleMotion(self, e):

        self.c.delete('temp_objects')
        self.c.create_rectangle(self.lineStartX, self.lineStartY, e.x, e.y, outline=self.color_fg, width=self.penwidth, tags='temp_objects')

    def drawOvalMotion(self,e):
        self.c.delete('temp_objects')
        self.c.create_oval(self.lineStartX, self.lineStartY, e.x, e.y, outline=self.color_fg, width=self.penwidth,
                                tags='temp_objects')

    def endLineDraw(self, e):
        self.c.delete('temp_objects')

        self.old_x = None
        self.old_y = None

        x = self.c.create_line(self.lineStartX, self.lineStartY, e.x, e.y, fill=self.color_fg, width=self.penwidth,
                               smooth=1)
        self.Line_objects.append(x)
        self.stack.append(self.Line_objects)
        self.Line_objects = []

    def endBrushDraw(self, e):
        self.stack.append(self.brushObjets)
        self.brushObjets = []

    def endRectangleDraw(self, e):
        self.c.delete('temp_objects')
        self.old_x = None
        self.old_y = None

        x = self.c.create_rectangle(self.lineStartX, self.lineStartY, e.x, e.y, outline=self.color_fg, width=self.penwidth)
        self.Line_objects.append(x)
        self.stack.append(self.Line_objects)
        self.Line_objects = []

    def endOvalDraw(self,e):
        self.c.delete('temp_objects')
        self.old_x = None
        self.old_y = None

        x = self.c.create_oval(self.lineStartX, self.lineStartY, e.x, e.y, outline=self.color_fg, width=self.penwidth)
        self.Line_objects.append(x)
        self.stack.append(self.Line_objects)
        self.Line_objects = []


    def changeW(self, e):  # change Width of pen through slider
        self.penwidth = e

    def clear(self):
        self.c.delete(ALL)

    def change_fg(self):  # changing the pen color
        aux = colorchooser.askcolor(color=self.color_fg)[1]
        if aux is not None:
            self.color_fg = aux
        self.refresh_colors()

    def change_fg2(self):
        aux = colorchooser.askcolor(color=self.color_fg2)[1]
        if aux is not None:
            self.color_fg2 = aux
        self.refresh_colors()

    def change_bg(self):  # changing the background color canvas
        aux = colorchooser.askcolor(color=self.color_bg)[1]
        if aux is not None:
            self.color_bg = aux
        self.c['bg'] = self.color_bg

    def refresh_colors(self):
        self.selectedColor = Button(self.colors, bg=self.color_fg, width=12, height=3, anchor="w",
                                    activebackground=self.color_fg, command=self.change_fg)
        self.selectedColor.grid(row=0, column=1)
        self.secondaryColor = Button(self.colors, bg=self.color_fg2, width=12, height=3, anchor="w",
                                     activebackground=self.color_fg2, command=self.change_fg2)
        self.secondaryColor.grid(row=1, column=1)

    def flip_colors(self):
        self.color_fg, self.color_fg2 = self.color_fg2, self.color_fg
        self.refresh_colors()

    def undo(self):
        x = self.stack.pop()
        self.redoStack.append(x)
        for i in x:
            self.c.delete(i)


    def redo(self):
        x = self.redoStack.pop()
        for i in x:
            self.c.
        self.stack.append(x)

    def drawWidgets(self):
        # controls
        self.controls = Frame(self.master, padx=5, pady=5)
        self.controls.config(bd=5, relief="groove")
        self.controls.pack(side=LEFT, expand=False, fill=Y)

        self.size = Frame(self.controls, padx=5, pady=5)
        Label(self.size, text='Pen Width:', font=('arial 12')).grid(row=0, column=0)
        self.slider = ttk.Scale(self.size, from_=5, to=100, command=self.changeW, orient=HORIZONTAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=0, column=1, ipadx=20)
        self.size.grid(row=1)

        self.colors = Frame(self.controls, padx=5, pady=5)
        Label(self.colors, text='Pen Color:', font=('arial 12')).grid(row=0, column=0)
        self.refresh_colors()
        self.flipcolor = Button(self.colors, text="Flip Colors", command=self.flip_colors)
        self.flipcolor.grid(row=1, column=0)
        self.colors.grid(row=2)

        self.toolsPanel = Frame(self.colors, padx=5, pady=5)
        Label(self.toolsPanel, text='Tools:', font=('arial 12')).grid(row=0, column=0)
        Button(self.toolsPanel, text='Brush', command=(lambda: self.changeTool(0))).grid(row=1, column=0)
        Button(self.toolsPanel, text='Line', command=(lambda: self.changeTool(1))).grid(row=1, column=1)
        Button(self.toolsPanel, text='Rectangle', command=(lambda: self.changeTool(2))).grid(row=2, column=0)
        Button(self.toolsPanel, text='Oval', command=(lambda: self.changeTool(3))).grid(row=2, column=1)
        self.toolsPanel.grid(row=3)

        # canvas
        self.base = Frame(self.master, padx=5, pady=5)
        self.base.pack(fill=BOTH, expand=True)
        self.c = Canvas(self.base, width=800, height=600, bg=self.color_bg)
        self.c.pack(fill=NONE, expand=True)

        # menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        filemenu = Menu(menu)
        colormenu = Menu(menu)
        editmenu = Menu(menu)

        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New', command='')
        filemenu.add_command(label='Open', command='')
        filemenu.add_command(label='Save', command='')
        filemenu.add_command(label='Save as', command='')
        filemenu.add_command(label='Export', command='')
        filemenu.add_command(label='Close', command='')
        filemenu.add_command(label='Quit', command=self.master.destroy)

        menu.add_cascade(label='Edit', menu=editmenu)
        editmenu.add_command(label='Undo', command=self.undo)
        editmenu.add_command(label='Redo', command=self.redo)
        editmenu.add_command(label='Import')
        editmenu.add_command(label='Clear Canvas', command=self.clear)

        menu.add_cascade(label='Colors', menu=colormenu)
        colormenu.add_command(label='Brush Color', command=self.change_fg)
        colormenu.add_command(label='Background Color', command=self.change_bg)


if __name__ == '__main__':
    root = Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    main(root)
    root.title('AImation')
    root.mainloop()
