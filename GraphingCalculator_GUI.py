#this file is the GUI for the graphing calculator that integrates all of the
#backend features of the project

import math
import decimal
import copy

from tkinter import *
#from Utility import *
from Terms import*
from Statistics import *
from numpy import*

class Graph(object):
    
    def __init__(self, axes, functions):
        self.axes = axes
        self.functions = functions
        
    def draw(self, Gui):
        lines = []
        self.axes.draw(Gui.canvas, Gui.canvasWidth, Gui.canvasHeight)
        for function in self.functions:
            function.draw(Gui.canvas, self.axes, \
            Gui.canvasWidth, Gui.canvasHeight)
        return lines
        
        
def init(self,master):
    self.canvas = Canvas(master, width = self.canvasWidth, \
    height = self.canvasHeight)
    self.canvas.pack(side = RIGHT, fill = BOTH)
    
    
    self.cartesianAxes = Axes()
    self.cartesianFunctions = []
    self.cartesianGraph = Graph(self.cartesianAxes, self.cartesianFunctions)
    self.cartesianPoints = []#math points
    
    self.highlightedEntry = 1
    self.mode = "cartesian"
    self.locationClicked = None
    self.locationReleased = None
    self.dragCount = 0
    self.selectedFunction = None
    self.point = None
    self.pointText = None
    self.pointBox = None
    self.canvasSelected = False
    self.lines = None
    self.selectedPoints = []
    self.selectedPointsText = []
    self.selectedPointsBoxes = []
    self.functionButtons = None
    self.drawPointsButton = None
    self.clearAllButton = None

    
    self.polarAxes = Axes()
    self.polarFunctions = []
    self.polarGraph = Graph(self.polarAxes, self.polarFunctions)
    
    self.parametricAxes = Axes()
    self.parametricFunctions = []
    self.parametricGraph = Graph(self.parametricAxes, self.parametricFunctions)
    
    
    self.scatterPlot = None
    self.statsEntryBox = None
    
        
def run ():
    
    def addUnicodeCharacter(self, char):
        index = self.highlightedEntry-1
        if index == -1:
            entry = self.statsEntryBox
        elif -1 <index < 6:
            entry = self.entries[index]
        else:
            entry = self.windowEntries[index-6]
        
       
        entry.insert(INSERT, char)
        
    def setHighlightedEntry(self, value):
        self.highlightedEntry = value
        
        
    def redrawAll(self, statsRescale = False):
        if self.mode == "cartesian":
            self.canvas.delete(ALL)
            self.cartesianFunctions = []
            self.cartesianPoints = []
            center = (self.cartesianAxes.xMax + self.cartesianAxes.xMin)/2
            for i in range (6):
                entry = self.entries[i]
                function = entry.get()
                
                try:
                    
                    functionObject = Sum((parseFunction(function, 'x',center)))
                    functionObject.setColor(self.colors[i])
                    self.cartesianFunctions.append(functionObject)
                    
                    if "d/dx" in function:
                        entry.delete(0, END)
                        entry.insert(0, str(functionObject))
                    
                        
                
                except:
                    
                    if len(entry.get()) > 0:
                        entry.delete(0, END)
                        entry.insert(len(entry.get()), "(invalid function)")
                
            
            self.cartesianGraph = Graph(self.cartesianAxes, \
            self.cartesianFunctions)
            self.lines = self.cartesianGraph.draw(self)
            
            self.cartesianPoints += findAllImportantPoint(\
            self.cartesianFunctions, self.cartesianAxes.xMin, \
            self.cartesianAxes.xMax)
            
            drawPoints(self.cartesianPoints, \
            self.canvas, self.cartesianAxes, self.canvasWidth, \
            self.canvasHeight, color = "grey")
            
        elif self.mode == "polar":
            self.canvas.delete(ALL)
            self.cartesianFunctions = []
            self.cartesianPoints = []
            center = (self.cartesianAxes.xMax + self.cartesianAxes.xMin)/2
            for i in range (6):
                entry = self.entries[i]
                function = entry.get()
                
                
                try:
                    
                    functionObject = Polar(parseFunction(function, \
                    u"\u03F4", center), 0, 16*3.14159)
                    functionObject.setColor(self.colors[i])
                    self.cartesianFunctions.append(functionObject)
                    
                    if "d/dx" in function:
                        entry.delete(0, END)
                        entry.insert(0, str(functionObject))
                    
                        
                
                except:
                    
                    if len(entry.get()) > 0:
                        entry.delete(0, END)
                        entry.insert(len(entry.get()), "(invalid function)")
                
            
            self.cartesianGraph = Graph(self.cartesianAxes, \
            self.cartesianFunctions)
            self.lines = self.cartesianGraph.draw(self)
            
            
        elif self.mode == "statistics":
            self.cartesianPoints = []
            self.cartesianFunctions = []
            try:
                data = self.statsEntryBox.get("1.0", END)
                self.cartesianPoints +=  parseStatsData(data)
                self.scatterPlot = ScatterPlot(self.cartesianPoints)
                self.cartesianFunctions += (\
                [self.scatterPlot.calculateRegression()])
                
                if not statsRescale:
                    self.scatterPlot.autoSetAxes(self.cartesianAxes)
                    updateWindowEntries(self)
                
                self.canvas.delete(ALL)
                self.cartesianGraph = Graph(self.cartesianAxes, \
                self.cartesianFunctions)
                self.lines = self.cartesianGraph.draw(self)
                                
                drawPoints(self.cartesianPoints, self.canvas, \
                self.cartesianAxes, self.canvasWidth, self.canvasHeight, \
                color = "red")
                
                self.scatterPlot.drawRegressionInfo( self.canvas, \
                self.canvasHeight)
                
                
            
            except:
                if len(data) > 0:
                    self.statsEntryBox.delete("1.0", END)
                    self.statsEntryBox.insert("1.0", "(invalid data)")
            
        elif self.mode == "parametric":
            self.canvas.delete(ALL)
            self.cartesianFunctions = []
            self.cartesianPoints = []
            center = (self.cartesianAxes.xMax + self.cartesianAxes.xMin)/2
            xMin = self.cartesianAxes.xMin
            xMax = self.cartesianAxes.xMax
            
            for i in range (3):
                entry = self.entries[2*i]
                entry2 = self.entries[2*i+1]
                function = entry.get()
                function2 = entry2.get()
                isValidFunction = True
                try:
                    functionObject = parseFunction(function, 't', center)
                    
                    if "d/dx" in function:
                        entry.delete(0, END)
                        entry.insert(0, parametric.functionXtoString())
                except:
                    isValidFunction = False
                    if len(entry.get()) > 0:
                        entry.delete(0, END)
                        entry.insert(0, "(invalid function)")
                
                try:
                    functionObject2 = parseFunction(function2, 't', center)
                    
                    if "d/dx" in function2:
                        entry2.delete(0, END)
                        entry2.insert(0, parametric.functionYtoString())
                except:
                    isValidFunction = False
                    if len(entry2.get()) > 0:
                        entry2.delete(0, END)
                        entry2.insert(0, "(invalid function)")
                        
                if isValidFunction:
                    parametric = Parametric(functionObject, \
                    functionObject2, xMin, xMax)
                    if i == 2:
                        parametric.setColor(self.colors[5])
                    else:
                        parametric.setColor(self.colors[i])
                    self.cartesianFunctions.append(parametric)
                    
                    
            self.cartesianGraph = Graph(self.cartesianAxes, \
            self.cartesianFunctions)
            self.lines = self.cartesianGraph.draw(self)
        

    def shiftAxes(self, event):
        self.locationClicked = (event.x, event.y)
        
    def setLocationClicked(self,event):
        #print(self.locationClicked )
        self.locationReleased = (event.x, event.y)
        
        dxScreen = self.locationReleased[0] - self.locationClicked[0]
        dyScreen = self.locationReleased[1] - self.locationClicked[1]
        
        dx = dxScreen/self.canvasWidth*(self.cartesianAxes.xMax - \
        self.cartesianAxes.xMin)
        self.cartesianAxes.xMax -= dx
        self.cartesianAxes.xMin -= dx
        
        dy = dyScreen/self.canvasHeight*(self.cartesianAxes.yMax - \
        self.cartesianAxes.yMin)
        self.cartesianAxes.yMax += dy
        self.cartesianAxes.yMin += dy
        
        self.entries[6].delete(0, END)
        self.entries[6].insert(0, str(formatValue(self.cartesianAxes.xMin)))
        
        self.entries[7].delete(0, END)
        self.entries[7].insert(0, str(formatValue(self.cartesianAxes.xMax)))
        
        self.entries[8].delete(0, END)
        self.entries[8].insert(0, str(formatValue(self.cartesianAxes.yMin)))
        
        self.entries[9].delete(0, END)
        self.entries[9].insert(0, str(formatValue(self.cartesianAxes.yMax)))
    
        self.locationClicked = None
        redrawAll(self)
        
    def setWindow(self):
        values = []
        for i in range (len(self.windowEntries)): 
            windowEntry = self.windowEntries[i]
            try:
                s = windowEntry.get()
                
                val = parseValue(s).generatePoint(1)[1]
                #print(val)
            except:
                #print(i)
                if i < 4:
                    if i in [0,2]:
                        val = -10
                    else:
                        val = 10
                else:
                    val = 1
                    
                windowEntry.delete(0, END)
                windowEntry.insert(0, str(val))
            values += [val]
        xMin = values[0]
        xMax = values[1]
        yMin = values[2]
        yMax = values[3]
        xScale = values[4]
        yScale  = values[5]
        self.cartesianAxes = Axes(xMin, xMax, yMin, yMax, xScale, yScale)
        redrawAll(self)
        
    def graph(self):
        if self.mode != "statistics":
            setWindow(self)
            
    def plotRegression(self):
        redrawAll(self)
        
        
    def selectFunction(self,event):
        #self.canvasSelected = True
        if self.mode in ["cartesian", "statistics"]:
            x = event.x
            y = event.y
            mathPoint = convertPointInverse((x,y),self.cartesianAxes, \
            self.canvasWidth, self.canvasHeight)
            #print(mathPoint)
            t = isNearIntersection((x,y), self)
            if t[0]:
                point = t[1]
                if point not in self.selectedPoints:
                    self.selectedPoints.append(point)
                    x = formatValue(point[0])
                    y = formatValue(point[1])
                    graphicsPoint = convertPoint(point, self.cartesianAxes, \
                    self.canvasWidth, self.canvasHeight)
                    gx = graphicsPoint[0]
                    gy = graphicsPoint[1]
                    d = 15
                    cx, cy = gx-d, gy-d
                    coordinate = "(%s,%s)" %(x,y)
                    dx = len(coordinate)*3
                    self.selectedPointsBoxes.append(\
                    self.canvas.create_rectangle(cx-dx, cy-8, \
                    cx+dx, cy+8, fill = "white"))
                    self.selectedPointsText.append(self.canvas.create_text(\
                    cx, cy, text = "(%s,%s)" %(x,y), font = "Times 12"))
                    
                else:
                    i = self.selectedPoints.index(point)
                    self.selectedPoints.pop(i)
                    text = self.selectedPointsText.pop(i)
                    self.canvas.delete(text)
                    box = self.selectedPointsBoxes.pop(i)
                    self.canvas.delete(box)
            
            else:
                for function in self.cartesianFunctions:
                    
                    dy = abs(function.generatePoint(mathPoint[0])[1] - \
                    mathPoint[1])
                    
                    dyScreen = dy/(self.cartesianAxes.yMax - \
                    self.cartesianAxes.yMin)*self.canvasHeight
                    #print(dyScreen)
                    if dyScreen < 12:
                        self.selectedFunction = function
                        
                        xVal = convertXInverse(event.x,self.cartesianAxes, \
                        self.canvasWidth, self.canvasHeight)
                        yVal = self.selectedFunction.generatePoint(xVal)[1]
                        
                        
                        t = convertPoint(\
                        self.selectedFunction.generatePoint(xVal), \
                        self.cartesianAxes, self.canvasWidth, 
                        self.canvasHeight)
                        
                        r = 10
                        rp = 20
                        
                        x = formatValue(xVal)
                        #print(x, xVal)
                        y = formatValue(\
                        self.selectedFunction.generatePoint(xVal)[1])
                        
                        
                        
                        coordinate = "(%s,%s)" %(x,y)
                        cx, cy = t[0]-rp, t[1]-rp
                        dx = len(coordinate)*3
                        
                        self.pointBox = self.canvas.create_rectangle(cx-dx, \
                        cy-8, cx+dx, cy+8, fill = "white")
                        self.point = self.canvas.create_oval(t[0]-r, t[1]-r,\
                         t[0]+r, t[1] + r, fill = self.selectedFunction.color,
                              width = 0)
                        self.pointText = self.canvas.create_text(t[0]-rp, \
                        t[1]-rp, text = coordinate, font = "Times 12")
                        
                        break
                        
                        
    def trackSelectedFunction(self, event):
        if self.mode in ["cartesian", "statistics"]:
            if self.selectedFunction != None:
                xVal = convertXInverse(event.x,self.cartesianAxes, \
                self.canvasWidth, self.canvasHeight)
                yVal = self.selectedFunction.generatePoint(xVal)[1]
                
                
                t = convertPoint(self.selectedFunction.generatePoint(xVal), \
                self.cartesianAxes, self.canvasWidth, self.canvasHeight)
                
                r = 5
                rp = 15
                
                x = formatValue(xVal)
                y = formatValue(self.selectedFunction.generatePoint(xVal)[1])
                
                self.canvas.coords(self.point, t[0]-r, t[1]-r,t[0]+r, t[1] + r)
                self.canvas.delete(self.pointText)
                self.canvas.delete(self.pointBox)
                coordinate = "(%s,%s)" %(x,y)
                cx, cy = t[0]-rp, t[1]-rp
                dx = len(coordinate)*3
                self.pointBox = self.canvas.create_rectangle(cx-dx, cy-8, \
                cx+dx, cy+8, fill = "white")
                self.pointText = self.canvas.create_text(t[0]-rp, t[1]-rp, \
                text = "(%s,%s)" %(x,y), font = "Times 12")
        
    def unselectFunction(self, event):
        if self.mode in ["cartesian", "statistics"]:
            self.canvas.delete(self.point)
            self.canvas.delete(self.pointText)
            self.canvas.delete(self.pointBox)
            self.selectedFunction = None
        
    def zoomOut(self):
        
        self.cartesianAxes.rescale(1.3)
        updateWindowEntries(self)
        redrawAll(self, True)
        
    def zoomIn(self):
        
        self.cartesianAxes.rescale(1/1.3)
        updateWindowEntries(self)
        redrawAll(self, True)
        
    #account for mode
    def updateWindowEntries(self):
        xMin = self.cartesianAxes.xMin
        xMax = self.cartesianAxes.xMax
        yMin = self.cartesianAxes.yMin
        yMax = self.cartesianAxes.yMax
        xScale = self.cartesianAxes.visualXScale
        yScale = self.cartesianAxes.visualYScale
        
        self.windowEntries[0].delete(0, END)
        self.windowEntries[0].insert(0, str(formatValue(xMin)))
        
        self.windowEntries[1].delete(0, END)
        self.windowEntries[1].insert(0, str(formatValue(xMax)))
        
        self.windowEntries[2].delete(0, END)
        self.windowEntries[2].insert(0, str(formatValue(yMin)))
        
        self.windowEntries[3].delete(0, END)
        self.windowEntries[3].insert(0, str(formatValue(yMax)))
        
        self.windowEntries[4].delete(0, END)
        self.windowEntries[4].insert(0, str(formatValue(xScale)))
        
        self.windowEntries[5].delete(0, END)
        self.windowEntries[5].insert(0, str(formatValue(yScale)))
        
    def clear(self):
        if self.mode != "statistics":
            for entry in self.entries:
                entry.delete(0, END)
            graph(self)
        else:
            self.statsEntryBox.delete("1.0", END)
            self.cartesianAxes = Axes()
            updateWindowEntries(self)
            redrawAll(self, True)
        
    
    def canvasNotSelected(self, event):
        #print("hey")
        self.canvasSelected = False
        
        
    def shiftGraph(self, direction):
        if direction == "Right":
            domain = self.cartesianAxes.xMax - self.cartesianAxes.xMin
            dx = domain*0.2
            self.cartesianAxes.xMax += dx
            self.cartesianAxes.xMin += dx
            
        elif direction == "Left":
            domain = self.cartesianAxes.xMax - self.cartesianAxes.xMin
            dx = domain*0.2
            self.cartesianAxes.xMax -= dx
            self.cartesianAxes.xMin -= dx
            
        elif direction == "Up":
            range = self.cartesianAxes.yMax - self.cartesianAxes.yMin
            dy = range*0.2
            self.cartesianAxes.yMax += dy
            self.cartesianAxes.yMin += dy
            
        elif direction == "Down":
            range = self.cartesianAxes.yMax - self.cartesianAxes.yMin
            dy = range*0.2
            self.cartesianAxes.yMax -= dy
            self.cartesianAxes.yMin -= dy
            
        updateWindowEntries(self)
        if self.mode == "statistics":
            redrawAll(self, True)
        else:
            redrawAll(self)
        
    def setMode(self, event):
       
        x = event.x
        y = event.y
        mode = ""
        
        if 0<=x<=150:
            if 0<=y<=50:
                mode = "cartesian"
            else:
                mode = "parametric"
        else:
            if 0<=y<=50:
                mode = "polar"
            else:
                mode = "statistics"
            
        
        previousMode = self.mode
        if previousMode != "statistics":
             clear(self)
        if self.mode != mode:
            self.mode = mode
            if self.mode == "cartesian":
                if previousMode == "statistics":
                    destroyStatsButtons(self)
                    self.statsEntryBox.destroy()
                    self.statsEntryBox = None
                    initCartesianEntries(self)
                    changeTitleBack(self)
                    redrawAll(self)
                else:
                    convertEntriesToCartesian(self)
            elif self.mode == "polar":
                if previousMode == "statistics":
                    destroyStatsButtons(self)
                    self.statsEntryBox.destroy()
                    self.statsEntryBox = None
                    initPolarEntries(self)
                    changeTitleBack(self)
                    redrawAll(self)
                else:
                    convertEntriesToPolar(self)
            elif self.mode == "parametric":
                if previousMode == "statistics":
                    destroyStatsButtons(self)
                    self.statsEntryBox.destroy()
                    self.statsEntryBox = None
                    initParametricEntries(self)
                    changeTitleBack(self)
                    redrawAll(self)
                else:
                    convertEntriesToParametric(self)
            elif self.mode == "statistics":
                destroyEntries(self)
                initStatsButtons(self)
                changeTitle(self)
                
                self.statsEntryBox = Text(self.functionPanel, width = 43, \
                height = 10, fg = "red", bg = "grey")
                self.statsEntryBox.grid(row = 1, columnspan = 2)
                self.statsEntryBox.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 0))
                   
    def destroyStatsButtons(self):
        self.drawPointsButton.destroy()
        
    def changeTitle(self):
        self.functionPanelTitleString.set("DATA")
        
    def changeTitleBack(self):
        self.functionPanelTitleString.set("FUNCTIONS")
        
    def initStatsButtons(self):
        self.drawPointsButton = Button (self.functionPanel, \
        text = "REGRESSION", width = 10)
        self.drawPointsButton.bind("<Button-1>", \
        lambda event:plotRegression(self))
        self.drawPointsButton.grid(row = 23,  columnspan = 2)
        
        
        
        
    def destroyFunctionButtons(self):
        #print(len(self.functionButtons))
        for i in range(6):
            self.functionButtons[i].destroy()
        
                    
    def convertEntriesToCartesian(self):
        newLabel = []
        for label in self.entryLabels:
            label.destroy()
        
        Y1 = Label(self.functionPanel, text = "Y" + u"\u2081=", \
        font = "Calibri 20", fg = self.colors[0])
        Y1.grid(row=1, column = 0)
        
        
        Y2 = Label(self.functionPanel, text = "Y" + u"\u2082=", \
        font = "Calibri 20", fg = self.colors[1])
        Y2.grid(row=2, column = 0)
        
        
        Y3 = Label(self.functionPanel, text = "Y" + u"\u2083=", \
        font = "Calibri 20", fg = self.colors[2])
        Y3.grid(row=3, column = 0)
        
        Y4 = Label(self.functionPanel, text = "Y" + u"\u2084=", \
        font = "Calibri 20", fg = self.colors[3])
        Y4.grid(row=4, column = 0)
        
        Y5 = Label(self.functionPanel, text = "Y" + u"\u2085=", \
        font = "Calibri 20", fg = self.colors[4])
        Y5.grid(row=5, column = 0)
        
        Y6 = Label(self.functionPanel, text = "Y" + u"\u2086=", \
        font = "Calibri 20", fg = self.colors[5])
        Y6.grid(row=6, column = 0)
        
        self.entryLabels = [Y1, Y2, Y3, Y4, Y5, Y6]
        
        self.cartesianAxes = Axes()
        updateWindowEntries(self)
        redrawAll(self)
        
    def initPolarEntries(self):
        R1 = Label(self.functionPanel, text = "R" + u"\u2081=", \
        font = "Calibri 20", fg = self.colors[0])
        Entry1 = Entry(self.functionPanel, width = 20)
        R1.grid(row=1, column = 0)
        Entry1.grid(row = 1, column = 1)
        
        R2 = Label(self.functionPanel, text = "R" + u"\u2082=", \
        font = "Calibri 20", fg = self.colors[1])
        Entry2 = Entry(self.functionPanel, width = 20)
        R2.grid(row=2, column = 0)
        Entry2.grid(row = 2, column = 1)
        
        R3 = Label(self.functionPanel, text = "R" + u"\u2083=", \
        font = "Calibri 20", fg = self.colors[2])
        Entry3 = Entry(self.functionPanel, width = 20)
        R3.grid(row=3, column = 0)
        Entry3.grid(row = 3, column = 1)
        
        R4 = Label(self.functionPanel, text = "R" + u"\u2084=", \
        font = "Calibri 20", fg = self.colors[3])
        Entry4 = Entry(self.functionPanel, width = 20)
        R4.grid(row=4, column = 0)
        Entry4.grid(row =4, column = 1)
        
        R5 = Label(self.functionPanel, text = "R" + u"\u2085=", \
        font = "Calibri 20", fg = self.colors[4])
        Entry5 = Entry(self.functionPanel, width = 20)
        R5.grid(row=5, column = 0)
        Entry5.grid(row = 5, column = 1)
        
        R6 = Label(self.functionPanel, text = "R" + u"\u2086=", \
        font = "Calibri 20", fg = self.colors[5])
        Entry6 = Entry(self.functionPanel, width = 20)
        R6.grid(row=6, column = 0)
        Entry6.grid(row = 6, column = 1)
        
        self.entries= [Entry1,Entry2, Entry3, Entry4, Entry5, Entry6] 
        self.entryLabels = [R1, R2, R3, R4, R5, R6]
        
        Entry1.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 1))
                                
        Entry2.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 2))
                                
        Entry3.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 3))
                                
        Entry4.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 4))
                                
        Entry5.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 5))
                                
        Entry6.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 6))
                                
        initFunctionButtons(self)
        self.cartesianAxes = Axes()
        updateWindowEntries(self)
        
        
    def convertEntriesToPolar(self):
        newLabel = []
        for label in self.entryLabels:
            label.destroy()
        
        R1 = Label(self.functionPanel, text = "R" + u"\u2081=", \
        font = "Calibri 20", fg = self.colors[0])
        R1.grid(row=1, column = 0)
        
        
        R2 = Label(self.functionPanel, text = "R" + u"\u2082=", \
        font = "Calibri 20", fg = self.colors[1])
        R2.grid(row=2, column = 0)
        
        
        R3 = Label(self.functionPanel, text = "R" + u"\u2083=", \
        font = "Calibri 20", fg = self.colors[2])
        R3.grid(row=3, column = 0)
        
        R4 = Label(self.functionPanel, text = "R" + u"\u2084=", \
        font = "Calibri 20", fg = self.colors[3])
        R4.grid(row=4, column = 0)
        
        R5 = Label(self.functionPanel, text = "R" + u"\u2085=", \
        font = "Calibri 20", fg = self.colors[4])
        R5.grid(row=5, column = 0)
        
        R6 = Label(self.functionPanel, text = "R" + u"\u2086=", \
        font = "Calibri 20", fg = self.colors[5])
        R6.grid(row=6, column = 0)
        
        self.entryLabels = [R1, R2, R3, R4, R5, R6]
        
        self.cartesianAxes = Axes()
        updateWindowEntries(self)
        redrawAll(self)
        
    def initParametricEntries(self):
        X1 = Label(self.functionPanel, text = "X" + u"\u2081=", \
        font = "Calibri 20", fg = self.colors[0])
        Entry1 = Entry(self.functionPanel, width = 20)
        X1.grid(row=1, column = 0)
        Entry1.grid(row = 1, column = 1)
        
        Y1 = Label(self.functionPanel, text = "Y" + u"\u2081=", \
        font = "Calibri 20", fg = self.colors[0])
        Entry2 = Entry(self.functionPanel, width = 20)
        Y1.grid(row=2, column = 0)
        Entry2.grid(row = 2, column = 1)
        
        X2 = Label(self.functionPanel, text = "X" + u"\u2082=", \
        font = "Calibri 20", fg = self.colors[1])
        Entry3 = Entry(self.functionPanel, width = 20)
        X2.grid(row=3, column = 0)
        Entry3.grid(row = 3, column = 1)
        
        Y2 = Label(self.functionPanel, text = "Y" + u"\u2082=", \
        font = "Calibri 20", fg = self.colors[1])
        Entry4 = Entry(self.functionPanel, width = 20)
        Y2.grid(row=4, column = 0)
        Entry4.grid(row =4, column = 1)
        
        X3 = Label(self.functionPanel, text = "X" + u"\u2083=", \
        font = "Calibri 20", fg = self.colors[5])
        Entry5 = Entry(self.functionPanel, width = 20)
        X3.grid(row=5, column = 0)
        Entry5.grid(row = 5, column = 1)
        
        Y3 = Label(self.functionPanel, text = "Y" + u"\u2083=", \
        font = "Calibri 20", fg = self.colors[5])
        Entry6 = Entry(self.functionPanel, width = 20)
        Y3.grid(row=6, column = 0)
        Entry6.grid(row = 6, column = 1)
        
        self.entries= [Entry1,Entry2, Entry3, Entry4, Entry5, Entry6] 
        self.entryLabels = [X1, Y1, X2, Y2,X3, Y3]
        
        Entry1.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 1))
                                
        Entry2.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 2))
                                
        Entry3.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 3))
                                
        Entry4.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 4))
                                
        Entry5.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 5))
                                
        Entry6.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 6))
                                
        initFunctionButtons(self)
        self.cartesianAxes = Axes()
        updateWindowEntries(self)
        
                            
    def convertEntriesToParametric(self):
        newLabel = []
        for label in self.entryLabels:
            label.destroy()
        
        X1 = Label(self.functionPanel, text = "X" + u"\u2081=", \
        font = "Calibri 20", fg = self.colors[0])
        X1.grid(row=1, column = 0)
        
        
        Y1 = Label(self.functionPanel, text = "Y" + u"\u2081=", \
        font = "Calibri 20", fg = self.colors[0])
        Y1.grid(row=2, column = 0)
        
        
        X2 = Label(self.functionPanel, text = "X" + u"\u2082=", \
        font = "Calibri 20", fg = self.colors[1])
        X2.grid(row=3, column = 0)
        
        Y2 = Label(self.functionPanel, text = "Y" + u"\u2082=", \
        font = "Calibri 20", fg = self.colors[1])
        Y2.grid(row=4, column = 0)
        
        X3 = Label(self.functionPanel, text = "X" + u"\u2083=", \
        font = "Calibri 20", fg = self.colors[5])
        X3.grid(row=5, column = 0)
        
        Y3 = Label(self.functionPanel, text = "Y" + u"\u2083=", \
        font = "Calibri 20", fg = self.colors[5])
        Y3.grid(row=6, column = 0)
        
        self.entryLabels = [X1, Y1, X2, Y2, X3, Y3]
        self.cartesianAxes = Axes()
        updateWindowEntries(self)
        redrawAll(self)
        
    def destroyEntries(self):
        for i in range(6):
            self.entries[i].destroy()
            self.entryLabels[i].destroy()
        self.entryLabels = None
            
        
    def initCartesianEntries(self):
        
        Y1 = Label(self.functionPanel, text = "Y" + u"\u2081=", \
        font = "Calibri 20", fg = self.colors[0])
        Entry1 = Entry(self.functionPanel, width = 20)
        Y1.grid(row=1, column = 0)
        Entry1.grid(row = 1, column = 1)
        
        Y2 = Label(self.functionPanel, text = "Y" + u"\u2082=", \
        font = "Calibri 20", fg = self.colors[1])
        Entry2 = Entry(self.functionPanel, width = 20)
        Y2.grid(row=2, column = 0)
        Entry2.grid(row = 2, column = 1)
        
        Y3 = Label(self.functionPanel, text = "Y" + u"\u2083=", \
        font = "Calibri 20", fg = self.colors[2])
        Entry3 = Entry(self.functionPanel, width = 20)
        Y3.grid(row=3, column = 0)
        Entry3.grid(row = 3, column = 1)
        
        Y4 = Label(self.functionPanel, text = "Y" + u"\u2084=", \
        font = "Calibri 20", fg = self.colors[3])
        Entry4 = Entry(self.functionPanel, width = 20)
        Y4.grid(row=4, column = 0)
        Entry4.grid(row =4, column = 1)
        
        Y5 = Label(self.functionPanel, text = "Y" + u"\u2085=", \
        font = "Calibri 20", fg = self.colors[4])
        Entry5 = Entry(self.functionPanel, width = 20)
        Y5.grid(row=5, column = 0)
        Entry5.grid(row = 5, column = 1)
        
        Y6 = Label(self.functionPanel, text = "Y" + u"\u2086=", \
        font = "Calibri 20", fg = self.colors[5])
        Entry6 = Entry(self.functionPanel, width = 20)
        Y6.grid(row=6, column = 0)
        Entry6.grid(row = 6, column = 1)
        
        self.entries= [Entry1,Entry2, Entry3, Entry4, Entry5, Entry6] 
        self.entryLabels = [Y1, Y2, Y3, Y4, Y5, Y6]
        
        Entry1.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 1))
                                
        Entry2.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 2))
                                
        Entry3.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 3))
                                
        Entry4.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 4))
                                
        Entry5.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 5))
                                
        Entry6.bind("<Button-1>", lambda event:
                                setHighlightedEntry(self, 6))
                                
        initFunctionButtons(self)
        self.cartesianAxes = Axes()
        updateWindowEntries(self)
                    
    def initFunctionButtons(self):
        thetaButton = Button(self.functionPanel, text = u"\u03F4", width = 10)
        thetaButton.bind("<Button-1>", lambda event:
        addUnicodeCharacter(self, u"\u03F4"))
        thetaButton.grid(row = 7, column = 0)
    
        
        piButton = Button(self.functionPanel, text = u"\u03C0", width = 10)
        piButton.bind("<Button-1>", lambda event:
        addUnicodeCharacter(self, u"\u03C0"))
        piButton.grid(row = 7, column = 1)
        
        superscript2 = u"\u00B2"
        secondDerButton = Button(self.functionPanel, text  = "d%s/dx%s" %\
        (superscript2, superscript2), width = 10)
        secondDerButton.bind("<Button-1>", lambda event:
        addUnicodeCharacter(self,  "d/dx(d/dx( ))"))
        secondDerButton.grid(row = 8, column = 0)
        
        
        eButton = Button(self.functionPanel, text  = "e", width = 10)
        eButton.bind("<Button-1>", lambda event:
        addUnicodeCharacter(self,  "e"))
        eButton.grid(row = 8, column = 1)
        
        derivativeButton = Button(self.functionPanel, text  = "d/dx", \
        width = 10)
        derivativeButton.bind("<Button-1>", lambda event:
        addUnicodeCharacter(self,  "d/dx( )"))
        derivativeButton.grid(row = 9, column = 0)
        
        clearButton = Button(self.functionPanel, text  = "CLEAR ALL", \
        width = 10)
        clearButton.bind("<Button-1>", lambda event:
        clear(self))
        clearButton.grid(row = 9, column = 1)
        
        self.functionButtons = [thetaButton, piButton, secondDerButton, \
        eButton, derivativeButton, clearButton]
        #self.functionButtons[0].destroy()
        
    class GUI(object):pass
    
    self = GUI()
    self.canvasWidth = 1000
    self.canvasHeight = 800
    
    master = Tk()
    master.title("PLOT TWIST!")
    
    master.bind("<Return>", lambda event:
                            graph(self))
    
    buttonFrame = Frame(master, width = 200, height = 800)
    buttonFrame.pack(side = LEFT, fill = BOTH)
    

    self.functionPanel = Frame(buttonFrame, width = 200, height = 700)
    self.functionPanel.pack(side = TOP)
    
    self.functionPanelTitleString = StringVar()
    self.functionPanelTitle = Label(self.functionPanel, \
    textvariable = self.functionPanelTitleString, font = "Calibri 25 bold")
    self.functionPanelTitle.grid(row = 0, columnspan = 2)
    self.functionPanelTitleString.set("FUNCTIONS")
    
    
    self.colors = ["blue", "red", '#%02x%02x%02x' % (139,0,139), \
    '#%02x%02x%02x' % (255,0,255), '#%02x%02x%02x' % (255,127,80), \
    '#%02x%02x%02x' % (0,102,0)]

    
    Y1 = Label(self.functionPanel, text = "Y" + u"\u2081=", \
    font = "Calibri 20", fg = self.colors[0])
    Entry1 = Entry(self.functionPanel, width = 20)
    Y1.grid(row=1, column = 0)
    Entry1.grid(row = 1, column = 1)
    
    Y2 = Label(self.functionPanel, text = "Y" + u"\u2082=", \
    font = "Calibri 20", fg = self.colors[1])
    Entry2 = Entry(self.functionPanel, width = 20)
    Y2.grid(row=2, column = 0)
    Entry2.grid(row = 2, column = 1)
    
    Y3 = Label(self.functionPanel, text = "Y" + u"\u2083=", \
    font = "Calibri 20", fg = self.colors[2])
    Entry3 = Entry(self.functionPanel, width = 20)
    Y3.grid(row=3, column = 0)
    Entry3.grid(row = 3, column = 1)
    
    Y4 = Label(self.functionPanel, text = "Y" + u"\u2084=", \
    font = "Calibri 20", fg = self.colors[3])
    Entry4 = Entry(self.functionPanel, width = 20)
    Y4.grid(row=4, column = 0)
    Entry4.grid(row =4, column = 1)
    
    Y5 = Label(self.functionPanel, text = "Y" + u"\u2085=", \
    font = "Calibri 20", fg = self.colors[4])
    Entry5 = Entry(self.functionPanel, width = 20)
    Y5.grid(row=5, column = 0)
    Entry5.grid(row = 5, column = 1)
    
    Y6 = Label(self.functionPanel, text = "Y" + u"\u2086=", \
    font = "Calibri 20", fg = self.colors[5])
    Entry6 = Entry(self.functionPanel, width = 20)
    Y6.grid(row=6, column = 0)
    Entry6.grid(row = 6, column = 1)
    
    self.entries= [Entry1,Entry2, Entry3, Entry4, Entry5, Entry6] 
    self.entryLabels = [Y1, Y2, Y3, Y4, Y5, Y6]
    
    Entry1.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 1))
                            
    Entry2.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 2))
                            
    Entry3.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 3))
                            
    Entry4.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 4))
                            
    Entry5.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 5))
                            
    Entry6.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 6))
                            
    initFunctionButtons(self)
    self.cartesianAxes = Axes()
        
                            
                            
    init(self, master)
    
    initFunctionButtons(self)
    
   
                            
    self.canvas.bind("<Button-1>", lambda event:
                                selectFunction(self,event))
    self.canvas.bind("<B1-Motion>", lambda event:
                            trackSelectedFunction(self, event))
    self.canvas.bind("<ButtonRelease-1>", lambda event:
                            unselectFunction(self, event))
                     
    '''
    functionPanel.bind("<Button-1>", lambda event:
                            canvasNotSelected(self, event))
    '''
    
    '''
    master.bind("<Key>", lambda event:
                            keyPressed(self, event))
       
    '''

    
    windowPanelTitle = Label(self.functionPanel, \
    text = "WINDOW SETTINGS", font = "Calibri 25 bold")
    windowPanelTitle.grid(row=10, columnspan = 2)
    
    XMinLabel = Label(self.functionPanel, text = "Xmin =", font = "Calibri 20")
    XMinEntry = Entry(self.functionPanel, width = 8)
    XMinEntry.insert(0, str(self.cartesianAxes.xMin))
    XMinLabel.grid(row=11, column = 0)
    XMinEntry.grid(row = 11, column = 1, stick = W)
    
    XMaxLabel = Label(self.functionPanel, text = "Xmax =", font = "Calibri 20")
    XMaxEntry = Entry(self.functionPanel, width = 8)
    XMaxEntry.insert(0, str(self.cartesianAxes.xMax))
    XMaxLabel.grid(row=12, column = 0)
    XMaxEntry.grid(row = 12, column = 1, stick = W)
    
    YMinLabel = Label(self.functionPanel, text = "Ymin =", font = "Calibri 20")
    YMinEntry = Entry(self.functionPanel, width = 8)
    YMinEntry.insert(0, str(self.cartesianAxes.yMin))
    YMinLabel.grid(row=13, column = 0)
    YMinEntry.grid(row = 13, column = 1, stick = W)
    
    YMaxLabel = Label(self.functionPanel, text = "Ymax =", font = "Calibri 20")
    YMaxEntry = Entry(self.functionPanel, width = 8)
    YMaxEntry.insert(0, str(self.cartesianAxes.yMax))
    YMaxLabel.grid(row=14, column = 0)
    YMaxEntry.grid(row = 14, column = 1, stick = W)
    
    XScaleLabel = Label(self.functionPanel, text = "XScale =", \
    font = "Calibri 20")
    XScaleEntry = Entry(self.functionPanel, width = 8)
    XScaleEntry.insert(0, str(self.cartesianAxes.xScale))
    XScaleLabel.grid(row=15, column = 0)
    XScaleEntry.grid(row = 15, column = 1, stick = W)
    
    YScaleLabel = Label(self.functionPanel, text = "YScale =", \
    font = "Calibri 20")
    YScaleEntry = Entry(self.functionPanel, width = 8)
    YScaleEntry.insert(0, str(self.cartesianAxes.xScale))
    YScaleLabel.grid(row=16, column = 0)
    YScaleEntry.grid(row = 16, column = 1, stick = W)
    
    self.windowEntries = [XMinEntry, XMaxEntry, YMinEntry, \
    YMaxEntry, XScaleEntry, YScaleEntry]
    #self.entries += self.windowEntries
    
    XMinEntry.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 7))
                            
    XMaxEntry.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 8))
                            
    YMinEntry.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 9))
                            
    YMaxEntry.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 10))
                            
    XScaleEntry.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 11))
                            
    YScaleEntry.bind("<Button-1>", lambda event:
                            setHighlightedEntry(self, 12))
    
    '''
    windowButton = Button(functionPanel, text = "SET WINDOW!", width = 20)
    windowButton.bind("<Button-1>", lambda event:
    setWindow(self))
    windowButton.grid(row = 17, columnspan = 2)
    '''
    zoomOutButton = Button(self.functionPanel, text = "ZOOM OUT", width = 10)
    zoomOutButton.bind("<Button-1>", lambda event:
    zoomOut(self))
    zoomOutButton.grid(row = 18, column=0)
    
    zoomInButton = Button(self.functionPanel, text = "ZOOM IN", width = 10)
    zoomInButton.bind("<Button-1>", lambda event:
    zoomIn(self))
    zoomInButton.grid(row = 18, column=1)
    
    upButton = Button(self.functionPanel, text = "SHIFT UP", width = 10)
    upButton.bind("<Button-1>", lambda event:
    shiftGraph(self, "Up"))
    upButton.grid(row = 19, column=0)
    
    downButton = Button(self.functionPanel, text = "SHIFT DOWN", width = 10)
    downButton.bind("<Button-1>", lambda event:
    shiftGraph(self, "Down"))
    downButton.grid(row = 19, column=1)
    
    leftButton = Button(self.functionPanel, text = "SHIFT RIGHT", width = 10)
    leftButton.bind("<Button-1>", lambda event:
    shiftGraph(self, "Right"))
    leftButton.grid(row = 20, column=0)
    
    rightButton = Button(self.functionPanel, text = "SHIFT LEFT", \
    width = 10, bg = "red")
    rightButton.bind("<Button-1>", lambda event:
    shiftGraph(self, "Left"))
    rightButton.grid(row = 20, column=1)
    
   
    modeButtons = Canvas(buttonFrame, width = 300, height = 100)
    modeButtons.create_rectangle(0,0,150,50,fill = '#%02x%02x%02x' % \
    (102,84,94), width = 0)
    modeButtons.create_rectangle(150,0,300,50,fill = '#%02x%02x%02x' % \
    (163,145,147), width = 0)
    modeButtons.create_rectangle(0,50,150,100,fill = '#%02x%02x%02x' % \
    (170,111,115), width = 0)
    modeButtons.create_rectangle(150,50,300,100,fill = '#%02x%02x%02x' % \
    (238,169,144), width = 0)
    
    modeButtons.create_text(75, 25, text = "CARTESIAN", fill = "white", \
    font = "Calibri 20 bold")
    modeButtons.create_text(225, 25, text = "POLAR", fill = "white", \
    font = "Calibri 20 bold")
    modeButtons.create_text(75, 75, text = "PARAMETRIC", fill = "white", \
    font = "Calibri 20 bold")
    modeButtons.create_text(225, 75, text = "STATISTICS", fill = "white", \
    font = "Calibri 20 bold")
    modeButtons.pack(side = BOTTOM)
    

    modeButtons.bind("<Button-1>", lambda event: 
                                        setMode(self, event))
    redrawAll(self)
    master.mainloop()
    
    
run()