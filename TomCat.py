from tkinter import *
from PIL import Image
from PIL import ImageTk
import os
import random
import math


class data(object):
    # Model
    def __init__(self, width=1000, height=500):
        data.width = width
        data.height = height
        data.canvasWidth = width / 2
        data.canvasHeight = height / 5 * 4
        data.canvasCx = width / 4
        data.canvasCy = height / 2
        data.timerDelay = 10  # milliseconds
        data.images = dict()
        data.images['welcomeCat'] = ImageTk.PhotoImage(Image.open('welcome.jpg'))
        data.images['profile'] = ImageTk.PhotoImage(Image.open('profile.jpg').resize((100, 100)), Image.ANTIALIAS)
        data.images['leftCat'] = ImageTk.PhotoImage(Image.open('talkingtomrun.png').resize((50, 50), Image.ANTIALIAS))
        data.images['rightCat'] = ImageTk.PhotoImage(Image.open('talkingtomswim.png').resize((50, 50), Image.ANTIALIAS))
        data.images['undo'] = ImageTk.PhotoImage(Image.open('undo.jpg').resize((100, 100), Image.ANTIALIAS))
        data.images['redo'] = ImageTk.PhotoImage(Image.open('redo.jpg').resize((100, 100), Image.ANTIALIAS))
        data.images['refresh'] = ImageTk.PhotoImage(Image.open('refresh.png').resize((100, 100), Image.ANTIALIAS))
        data.dotShapes = get('dotShapes')
        data.commandShapes = get('commandShapes')
        data.code = []
        data.deletedDots = []
        data.dots = []
        data.route = []
        data.dxs = []
        data.dys = []
        data.dirs = []
        data.visited = []
        data.draw = False
        data.speed = 1
        data.radius = 10
        data.slice=36
        data.currentView = 'splashScreenView'


def get(path):
    shapes = {}
    for filename in os.listdir(path):
        image = Image.open(path + "/" + filename)
        shapes[filename[:-4]] = ImageTk.PhotoImage(image.resize((200, 200)))
    return shapes


class splashScreenView(Frame):
    def __init__(self, master, data):
        super().__init__(master.container)
        self.dotButton = Button(self, text="描点模式", height=2, width=10, font=("Times", 12, "bold"),
                                command=lambda: master.show_frame('dotPageView', data))
        self.commandButton = Button(self, text="命令模式", height=2, width=10, font=("Times", 12, "bold"),
                                    command=lambda: master.show_frame('commandPageView', data))
        self.dotButton.place(x=100, y=300)
        self.commandButton.place(x=300, y=300)
        self.image = Label(self, image=data.images['welcomeCat'])
        self.image.place(x=data.width / 4 * 3, y=data.height / 2, anchor='center')


class dotPageView(Frame):
    def __init__(self, master, data):
        super().__init__(master.container)
        self.canvas = Canvas(self, width=data.canvasWidth, height=data.canvasHeight, bg='white')
        self.canvas.place(x=data.canvasCx, y=data.canvasCy, anchor='center')

        self.refreshButton = Button(self, image=data.images['refresh'], command=lambda: master.refresh(data))
        self.paintButton = Button(self, image=data.images['profile'], font=("Times", 12, "bold"),
                                  command=lambda: master.dotGetRoute(data))
        self.undoButton = Button(self, image=data.images['undo'], command=lambda: master.undo(data))
        self.redoButton = Button(self, image=data.images['redo'], command=lambda: master.redo(data))

        self.refreshButton.place(x=data.width / 12 * 7, y=data.height / 12)
        self.paintButton.place(x=data.width / 12 * 8, y=data.height / 12)
        self.undoButton.place(x=data.width / 12 * 7, y=data.height / 12 * 3)
        self.redoButton.place(x=data.width / 12 * 8, y=data.height / 12 * 3)

        self.entry = Text(self, width=80, height=30, undo=True)
        self.entry.place(x=data.width / 4 * 3, y=data.height / 3 * 2, anchor='center')

        self.card = Label(self, image=random.choice(list(data.dotShapes.values())))
        self.card.place(x=data.width / 12 * 10, y=data.height / 12 * 3, anchor='center')


class commandPageView(Frame):
    def __init__(self, master, data):
        super().__init__(master.container)
        self.canvas = Canvas(self, width=data.canvasWidth, height=data.canvasHeight, bg='white')
        self.canvas.place(x=data.canvasCx, y=data.canvasCy, anchor='center')

        self.refreshButton = Button(self, image=data.images['refresh'], command=lambda: master.refresh(data))
        self.paintButton = Button(self, image=data.images['profile'], font=("Times", 12, "bold"),
                                  command=lambda: master.parseCode(data))
        self.undoButton = Button(self, image=data.images['undo'], command=lambda: master.undo(data))
        self.redoButton = Button(self, image=data.images['redo'], command=lambda: master.redo(data))

        self.refreshButton.place(x=data.width / 12 * 7, y=data.height / 12)
        self.paintButton.place(x=data.width / 12 * 8, y=data.height / 12)
        self.undoButton.place(x=data.width / 12 * 7, y=data.height / 12 * 3)
        self.redoButton.place(x=data.width / 12 * 8, y=data.height / 12 * 3)

        self.entry = Text(self, width=80, height=30, undo=True)
        self.entry.place(x=data.width / 4 * 3, y=data.height / 3 * 2, anchor='center')

        self.card = Label(self, image=random.choice(list(data.commandShapes.values())))
        self.card.place(x=data.width / 12 * 10, y=data.height / 12 * 3, anchor='center')


class Controller():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Talking Tom Cat")
        self.model = data(width, height)  # initialize the model
        self.container = Frame(self.root)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.views = {}
        for F in (splashScreenView, dotPageView, commandPageView):
            page_name = F.__name__
            view = F(self, data)
            self.views[page_name] = view
            view.grid(row=0, column=0, sticky="nsew")
        self.show_frame(data.currentView, data)
        self.root.bind("<Button-1>", lambda event: self.mousePressedWrapper(event, data))
        self.timerFiredWrapper(data)

    def show_frame(self, page_name, data):
        '''Show a frame for the given page name'''
        view = self.views[page_name]
        view.tkraise()
        view.winfo_toplevel().geometry("%dx%d" % (data.width, data.height))
        data.currentView = page_name

    def dotGetRoute(self, data):
        data.code = self.views['dotPageView'].entry.get('1.0', END).splitlines()
        for code in data.code:
            code = code.split(' ')
            start = data.dots[int(code[1]) - 1]
            end = data.dots[int(code[2]) - 1]
            data.route.append((start, end))
            startx, starty = start
            endx, endy = end
            distance = ((startx - endx)**2 + (starty - endy)**2)**0.5
            data.dxs.append(data.speed / distance * (endx - startx))
            data.dys.append(data.speed / distance * (endy - starty))
            data.dirs.append('right' if startx < endx else 'left')
        (data.start, data.end) = data.route[0]
        data.startx, data.starty = data.start
        data.dx = data.dxs[0]
        data.dy = data.dys[0]
        data.dir = data.dirs[0]
        data.draw = True
        print("dots: ", data.dots)
        print("route: ", data.route)

    def parseCode(self, data):
        data.code=self.views['commandPageView'].entry.get('1.0', END).splitlines()
        for code in data.code:
            if 'c' in code:
                code=code.split(' ')
                cx,cy=data.dots[int(code[1]) - 1]
                radius=int(code[2])
                for i in range(data.slice):
                    startAngle=i*math.pi*2/data.slice
                    endAngle=(i+1)*math.pi*2/data.slice
                    startx=cx + radius * math.cos(startAngle)
                    starty=cy - radius * math.sin(startAngle)
                    endx=cx + radius * math.cos(endAngle)
                    endy=cy - radius * math.sin(endAngle)
                    data.route.append(((startx,starty),(endx,endy)))
                    distance=((startx - endx)**2 + (starty - endy)**2)**0.5
                    data.dxs.append(data.speed / distance * (endx - startx))
                    data.dys.append(data.speed / distance * (endy - starty))
                    data.dirs.append('right' if startx < endx else 'left')
            if 'o' in code:
                code=code.split(' ')
                cx,cy=data.dots[int(code[1]) - 1]
                a=int(code[2])
                b=int(code[3])
                for i in range(data.slice):
                    startAngle=i*math.pi*2/data.slice
                    endAngle=(i+1)*math.pi*2/data.slice
                    startx=cx + a * math.cos(startAngle)
                    starty=cy - b * math.sin(startAngle)
                    endx=cx + a * math.cos(endAngle)
                    endy=cy - b * math.sin(endAngle)
                    data.route.append(((startx,starty),(endx,endy)))
                    distance=((startx - endx)**2 + (starty - endy)**2)**0.5
                    data.dxs.append(data.speed / distance * (endx - startx))
                    data.dys.append(data.speed / distance * (endy - starty))
                    data.dirs.append('right' if startx < endx else 'left')
        (data.start, data.end) = data.route[0]
        data.startx, data.starty = data.start
        data.dx = data.dxs[0]
        data.dy = data.dys[0]
        data.dir = data.dirs[0]
        data.draw = True
        print("dots: ", data.dots)
        print("route: ", data.route)





    def isNear(self, data):
        # needs to find a more robust way
        data.endx, data.endy = data.end
        if (((data.startx - data.endx)**2 + (data.starty - data.endy)**2)**0.5 < 10):
            return True
        else:
            return False

    def mousePressed(self, event, data):
        if (((event.x >= data.canvasCx - data.canvasWidth / 2) and (event.x <= data.canvasCx + data.canvasWidth / 2)) and
                ((event.y >= data.canvasCy - data.canvasHeight / 2) and (event.y <= data.canvasCy + data.canvasHeight / 2))):
            data.dots.append((event.x, event.y))

    def keyPressed(self, event, data):
        pass

    def timerFired(self, data):
        if data.draw:
            data.startx += data.dx
            data.starty += data.dy
            if self.isNear(data):
                try:
                    data.visited.append((data.start, data.end))
                    newIndex = data.route.index((data.start, data.end)) + 1
                    data.start, data.end = data.route[newIndex]
                    data.startx, data.starty = data.start
                    data.dx = data.dxs[newIndex]
                    data.dy = data.dys[newIndex]
                    data.dir = data.dirs[newIndex]
                except:
                    data.dx = 0
                    data.dy = 0

    def redrawAll(self, data):
        canvas = self.views[data.currentView].canvas
        for i in range(len(data.dots)):
            cx, cy = data.dots[i]
            x1, y1 = cx - data.radius, cy - data.radius
            x2, y2 = cx + data.radius, cy + data.radius
            canvas.create_oval(x1, y1, x2, y2, fill='red')
            canvas.create_text(cx, cy, text=str(i + 1),
                               font=("Times", 12, "bold"))
        if data.draw:
            if data.dir == 'right':
                canvas.create_image(data.startx, data.starty, image=data.images['rightCat'])
            elif data.dir == 'left':
                canvas.create_image(data.startx, data.starty, image=data.images['leftCat'])

            for start, end in data.visited:
                startx, starty = start
                endx, endy = end
                canvas.create_line(startx, starty, endx, endy, fill='purple', width=3)
            canvas.create_line(data.start, (data.startx, data.starty), fill='purple', width=3)



    def redo(self, data):
        data.dots.append(data.deletedDots.pop())

    def undo(self, data):
        data.deletedDots.append(data.dots.pop())

    def refresh(self, data):
        data.dots = []
        data.deletedDots = []
        data.visited = []
        data.route = []
        data.dxs = []
        data.dys = []
        data.dirs = []
        data.draw = False
        if data.currentView=='dotPageView':
            self.views['dotPageView'].card = Label(self.views['dotPageView'], image=random.choice(list(data.dotShapes.values())))
            self.views['dotPageView'].card.place(x=data.width / 12 * 10, y=data.height / 12 * 3, anchor='center')
            self.views['dotPageView'].canvas.delete(ALL)
            self.views['dotPageView'].canvas.update()
        elif data.currentView=='commandPageView':
            self.views['commandPageView'].card = Label(self.views['commandPageView'], image=random.choice(list(data.commandShapes.values())))
            self.views['commandPageView'].card.place(x=data.width / 12 * 10, y=data.height / 12 * 3, anchor='center')
            self.views['commandPageView'].canvas.delete(ALL)
            self.views['commandPageView'].canvas.update()

    def redrawAllWrapper(self, data):
        if data.currentView != 'splashScreenView':
            canvas = self.views[data.currentView].canvas
            canvas.delete(ALL)
            self.redrawAll(data)
            canvas.update()

    def mousePressedWrapper(self, event, data):
        self.mousePressed(event, data)
        self.redrawAllWrapper(data)

    def keyPressedWrapper(self, event, data):
        self.keyPressed(event, data)
        # if data.mode == 'command':
        #     commandMousePressed(event, data)
        self.redrawAllWrapper(data)

    def timerFiredWrapper(self, data):
        self.timerFired(data)
        self.redrawAllWrapper(data)
        if data.currentView != 'splashScreenView':
            self.views[data.currentView].canvas.after(data.timerDelay, self.timerFiredWrapper, data)
        else:
            self.views[data.currentView].after(data.timerDelay, self.timerFiredWrapper, data)


app = Controller(1600, 800)
app.root.mainloop()
print(data.commandShapes)
